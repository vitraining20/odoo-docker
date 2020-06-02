import logging
import functools
import werkzeug

from odoo import _
from odoo import http
from odoo.http import request
from odoo.tools import ustr
from odoo.osv import expression
from odoo.exceptions import UserError, AccessError, ValidationError

from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.portal.controllers.portal import CustomerPortal
from .controller_mixin import WSDControllerMixin

_logger = logging.getLogger(__name__)

GROUP_USER_ADVANCED = (
    'crnd_wsd.group_service_desk_website_user_advanced'
)

ITEMS_PER_PAGE = 20


# NOTE: here is name collision with request, so be careful, when use name
# `request`. To avoid this name collision use names `req` and reqs` for
# `request.request` records

def can_read_request(record):
    """
    This function check has user access to record.
    :param record: record
    :return: True or False
    """
    try:
        record = record.sudo(http.request.env.user)
        record.check_access_rights('read')
        record.check_access_rule('read')
    except AccessError:
        return False
    return True


def get_redirect():
    """
    This function returns quoted redirect parameter based on current page.
    It is used to redirect user on Login or Signup pages.

    For example, current URL is
    'http://localhost:11069/requests/new/step/category?service_id=1'

    >>> get_redirect()
    ... redirect=%2Frequests%2Fnew%2Fstep%2Fcategory%3Fservice_id%3D1

    Result of this function could be used to redirect user to
    login page and redirect to same page after login. For example:

    >>> redirect_url = "/web/login?%s" % get_redirect()
    >>> redirect_url
    ... "/web/login?redirect=
    ... %2Frequests%2Fnew%2Fstep%2Fcategory%3Fservice_id%3D1

    Note, that 'redirect' param has quoted value that allows to keep
    query parametrs.
    """

    full_url = request.httprequest.url
    host = request.httprequest.environ['HTTP_HOST']
    url = full_url.split(host)[1]
    return werkzeug.urls.url_encode({'redirect': url})


def guard_access(func):
    """
    This is a decorator function. It is used to redirect public users
    to Login page if the 'request_wsd_public_ui_visibility' field is set
    to 'redirect' in the settings. Once logged in, users will be redirected
    back to the targeted page.

    Use it to decorate functions with '@http.route' decorator, on the
    required routes. When a user trying to access specified route, he will
    be checked by @guard_access conditions first.

    How to use: place '@guard_access' after '@http.route' decorator, before
    decorated function. For example:
    >>>@http.route(["/requests/new"], type='http', auth="public",
    ...            methods=['GET'], website=True)
    ...@guard_access
    ...def request_new(self, **kwargs):
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not request.website.is_public_user():
            return func(*args, **kwargs)
        if (request.env.user.company_id.request_wsd_public_ui_visibility ==
                'redirect'):
            url = "/web/login?%s" % get_redirect()
            return request.redirect(url)
        return func(*args, **kwargs)
    return wrapper


class WebsiteRequest(WSDControllerMixin, http.Controller):
    def _requests_get_request_domain_base(self, search, kind_id=None, **post):
        domain = []
        if search:
            domain += [
                '|', '|', '|', ('name', 'ilike', search),
                ('category_id.name', 'ilike', search),
                ('type_id.name', 'ilike', search),
                ('request_text', 'ilike', search)]

        kind = self._id_to_record('request.kind', kind_id, no_raise=True)
        if kind:
            domain = expression.AND([
                domain,
                [('kind_id', '=', kind.id)],
            ])

        return domain

    def _requests_get_request_domains(self, search, **post):
        domain = self._requests_get_request_domain_base(search, **post)

        return {
            'all': domain,
            'open': domain + [('closed', '=', False)],
            'closed': domain + [('closed', '=', True)],
            'my': domain + [
                ('closed', '=', False),
                '|', '|',
                ('user_id', '=', request.env.user.id),
                ('created_by_id', '=', request.env.user.id),
                ('author_id', '=', request.env.user.partner_id.id),
            ],
        }

    def _requests_list_get_extra_context(self, req_status, search, **post):
        selected_request_kind = self._id_to_record(
            'request.kind', post.get('kind_id'), no_raise=True)
        request_kinds = http.request.env['request.kind'].search([
            ('show_as_website_filter', '=', True),
            ('request_ids', '!=', False),
        ]).filtered(lambda r: r.request_ids)

        return {
            'request_kinds': request_kinds,
            'selected_request_kind': selected_request_kind,
        }

    def _request_page_get_extra_context(self, req_id, **post):
        return {}

    @http.route(['/requests',
                 '/requests/<string:req_status>',
                 '/requests/<string:req_status>/page/<int:page>'],
                type='http', auth="public", website=True)
    @guard_access
    def requests(self, req_status='my', page=0, search="", **post):
        if req_status not in ('my', 'open', 'closed', 'all'):
            return request.not_found()

        Request = request.env['request.request']

        url = '/requests/' + req_status
        keep = QueryURL(
            url, [], search=search, **post)
        domains = self._requests_get_request_domains(search, **post)

        req_count = {
            'all': Request.search_count(domains['all']),
            'open': Request.search_count(domains['open']),
            'closed': Request.search_count(domains['closed']),
            'my': Request.search_count(domains['my']),
        }

        # make pager
        pager = request.website.pager(
            url=url,
            total=req_count[req_status],
            page=page,
            step=ITEMS_PER_PAGE,
            url_args=dict(
                post, search=search),
        )

        # search the count to display, according to the pager data
        reqs = request.env['request.request'].search(
            domains[req_status], limit=ITEMS_PER_PAGE, offset=pager['offset'])
        values = {
            'search': search,
            'reqs': reqs.sudo(),
            'pager': pager,
            'default_url': url,
            'req_status': req_status,
            'req_count': req_count,
            'keep': keep,
            'get_redirect': get_redirect,
        }

        values.update(self._requests_list_get_extra_context(
            req_status=req_status, search=search, **post
        ))
        return request.render(
            'crnd_wsd.wsd_requests', values)

    def _request_get_available_routes(self, req, **post):
        Route = http.request.env['request.stage.route']
        result = Route.browse()

        user = http.request.env.user
        group_ids = user.sudo().groups_id.ids
        action_routes = Route.search(expression.AND([
            [('request_type_id', '=', req.sudo().type_id.id)],
            [('stage_from_id', '=', req.sudo().stage_id.id)],
            [('website_published', '=', True)],
            expression.OR([
                [('allowed_user_ids', '=', False)],
                [('allowed_user_ids', '=', user.id)],
            ]),
            expression.OR([
                [('allowed_group_ids', '=', False)],
                [('allowed_group_ids', 'in', group_ids)],
            ]),
        ]))

        for route in action_routes:
            try:
                route._ensure_can_move(req)
            except AccessError:  # pylint: disable=except-pass
                pass
            except ValidationError:  # pylint: disable=except-pass
                pass
            else:
                result += route
        return result

    @http.route(["/requests/request/<int:req_id>"],
                type='http', auth="user", website=True)
    def request(self, req_id, **kw):
        values = {}
        reqs = request.env['request.request'].search(
            [('id', '=', req_id)])

        if not reqs:
            raise request.not_found()

        reqs.check_access_rights('read')
        reqs.check_access_rule('read')

        action_routes = self._request_get_available_routes(reqs, **kw)

        disable_new_comments = (
            reqs.closed and reqs.sudo().type_id.website_comments_closed
        )

        values.update({
            'req': reqs.sudo(),
            'action_routes': action_routes.sudo(),
            'can_change_request_text': reqs.can_change_request_text,
            'disable_composer': disable_new_comments,
            'can_read_request': can_read_request,
        })

        values.update(self._request_page_get_extra_context(req_id, **kw))

        return request.render(
            "crnd_wsd.wsd_request", values)

    @http.route(["/requests/new"], type='http', auth="public",
                methods=['GET'], website=True)
    @guard_access
    def request_new(self, **kwargs):
        # May be overridden to change start step
        return request.redirect(QueryURL(
            '/requests/new/step/category', [])(**kwargs))

    def _request_new_get_public_categs_domain(self, category_id=None, **post):
        if request.env.user.has_group(GROUP_USER_ADVANCED):
            return []
        return [('website_published', '=', True)]

    def _request_new_get_public_categs(self, category_id=None, **post):
        categs = request.env['request.category'].search(
            self._request_new_get_public_categs_domain(
                category_id=category_id, **post))
        return categs.filtered(
            lambda r: self._request_new_get_public_types(
                category_id=r.id, **post))

    @http.route(["/requests/new/step/category"], type='http', auth="public",
                methods=['GET', 'POST'], website=True)
    @guard_access
    def request_new_select_category(self, category_id=None, **kwargs):
        keep = QueryURL('', [], category_id=category_id, **kwargs)
        req_category = self._id_to_record('request.category', category_id)
        if request.httprequest.method == 'POST' and req_category:
            return request.redirect(keep(
                '/requests/new/step/type',
                category_id=req_category.id, **kwargs))

        public_categories = self._request_new_get_public_categs(
            category_id=category_id, **kwargs).filtered(
                lambda r: self._request_new_get_public_types(
                    category_id=r.id, **kwargs))

        if len(public_categories) <= 1 and not http.request.session.debug:
            return request.redirect(keep(
                '/requests/new/step/type',
                category_id=public_categories.id, **kwargs))

        values = {
            'req_categories': public_categories,
            'req_category_sel': req_category,
            'keep': keep,
            'get_redirect': get_redirect,
        }

        return request.render(
            "crnd_wsd.wsd_requests_new_select_category", values)

    def _request_new_get_public_types(self, type_id=None, category_id=None,
                                      **kwargs):
        domain = []
        if not request.env.user.has_group(GROUP_USER_ADVANCED):
            domain += [('website_published', '=', True)]

        if category_id:
            domain += [('category_ids.id', '=', category_id)]
        else:
            domain += [('category_ids', '=', False)]

        return request.env['request.type'].search(domain)

    @http.route(["/requests/new/step/type"], type='http', auth="public",
                methods=['GET', 'POST'], website=True)
    @guard_access
    def request_new_select_type(self, type_id=None, category_id=None,
                                **kwargs):
        keep = QueryURL('', [], type_id=type_id, category_id=category_id,
                        **kwargs)
        req_type = self._id_to_record('request.type', type_id)
        req_category = self._id_to_record('request.category', category_id)
        if request.httprequest.method == 'POST' and req_type:
            return request.redirect(keep(
                '/requests/new/step/data', type_id=req_type.id,
                category_id=req_category.id, **kwargs))

        public_types = self._request_new_get_public_types(
            type_id=type_id, category_id=req_category.id, **kwargs)

        if len(public_types) == 1 and not http.request.session.debug:
            return request.redirect(keep(
                '/requests/new/step/data', type_id=public_types.id,
                category_id=req_category.id, **kwargs))

        values = {
            'req_types': public_types,
            'req_type_sel': req_type,
            'req_category': req_category,
            'keep': keep,
            'get_redirect': get_redirect,
        }

        return request.render(
            "crnd_wsd.wsd_requests_new_select_type", values)

    def _request_new_process_data(self, req_type, req_category=False,
                                  req_text=None, **post):
        return {
            'req_type': req_type,
            'req_category': req_category,
            'req_text': req_text,
        }

    def _request_new_validate_data(self, req_type, req_category,
                                   req_text, data, **post):
        errors = []
        if not req_text or req_text == '<p><br></p>':
            errors.append(_(
                "Request text is empty!"))
        return errors

    def _request_new_prepare_data(self, req_type, req_category,
                                  req_text, **post):
        return {
            'category_id': req_category and req_category.id,
            'type_id': req_type.id,
            'request_text': req_text,
        }

    @http.route(["/requests/new/step/data"],
                type='http', auth="public",
                methods=['GET', 'POST'], website=True)
    @guard_access
    def request_new_fill_data(self, type_id=None, category_id=None,
                              req_text=None, **kwargs):
        req_type = self._id_to_record('request.type', type_id)

        if not req_type:
            return request.redirect(QueryURL(
                '/requests/new/step/type', [])(
                    type_id=type_id, category_id=category_id, **kwargs))

        req_category = self._id_to_record('request.category', category_id)

        values = self._request_new_process_data(
            req_type, req_category, req_text=req_text, **kwargs)
        values.update({
            'get_redirect': get_redirect,
        })

        if request.httprequest.method == 'POST':
            req_data = self._request_new_prepare_data(
                req_type, req_category, req_text, **kwargs)

            validation_errors = self._request_new_validate_data(
                req_type, req_category, req_text, req_data, **kwargs)

            if not validation_errors:
                try:
                    req = request.env['request.request'].create(req_data)
                except (UserError, AccessError, ValidationError) as exc:
                    validation_errors.append(ustr(exc))
                except Exception:
                    _logger.error(
                        "Error caught during request creation", exc_info=True)
                    validation_errors.append(
                        _("Unknown server error. See server logs."))
                else:
                    return request.render(
                        "crnd_wsd.wsd_requests_new_congratulation",
                        {'req': req.sudo()})

            values['validation_errors'] = validation_errors
            # TODO: update values with posted values to save data entered by
            # user
        return request.render(
            "crnd_wsd.wsd_requests_new_request_data", values)


class RequestCustomerPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(
            RequestCustomerPortal, self)._prepare_portal_layout_values()
        user = request.env.user
        values['request_count'] = request.env['request.request'].search_count(
            ['|', '|', ('created_by_id', '=', user.id),
             ('user_id', '=', user.id),
             ('partner_id', 'child_of',
              user.partner_id.commercial_partner_id.id)])
        return values

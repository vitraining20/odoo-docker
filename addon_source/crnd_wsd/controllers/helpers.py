import io
import json
import base64
import logging
from PIL import Image

from odoo import http, tools, _
from odoo.tools import ustr
from odoo.http import request

from .controller_mixin import WSDControllerMixin

_logger = logging.getLogger(__name__)


class WSDHelpers(WSDControllerMixin, http.Controller):

    def _optimize_image(self, image_data, disable_optimization=False):
        try:
            image = Image.open(io.BytesIO(image_data))
            w, h = image.size
            if w * h >= 42e6:  # Nokia Lumia 1020 photo resolution
                raise ValueError(_(
                    u"Image size excessive, uploaded images "
                    u"must be smaller than 42 million pixel"))
            if not disable_optimization and image.format in ('PNG', 'JPEG'):
                image_data = tools.image_save_for_web(image)
        except IOError:  # pylint: disable=except-pass
            pass
        return image_data

    @http.route('/crnd_wsd/file_upload', type='http',
                auth='user', methods=['POST'], website=True)
    def wsd_upload_file(self, upload, alt='File', filename=None,
                        is_image=False, **post_data):
        Attachments = request.env['ir.attachment']

        # TODO: bound attachemnts to request
        try:
            data = upload.read()

            if is_image:
                data = self._optimize_image(data, disable_optimization=False)

            attachment = Attachments.create({
                'name': alt,
                'datas': base64.b64encode(data),
                'datas_fname': filename or 'upload',
                'public': True,   # TODO: should it be public?
                # 'res_model': 'ir.ui.view',
            })
        except Exception as e:
            _logger.exception("Failed to upload file to attachment")
            message = ustr(e)
            return json.dumps({
                'status': 'FAIL',
                'success': False,
                'message': message,
            })

        if is_image:
            attachment_url = "/web/image/%d/%s" % (
                attachment.id,
                attachment.datas_fname,
            )
        else:
            attachment_url = "/web/content/%d/%s" % (
                attachment.id,
                attachment.datas_fname,
            )

        return json.dumps({
            'status': 'OK',
            'success': True,
            'attachment_url': attachment_url,
        })

    @http.route('/crnd_wsd/api/request/update-text', type='json',
                auth='user', methods=['POST'], website=True)
    def wsd_request_update_text(self, request_id, request_text):
        try:
            reqs = self._id_to_record('request.request', request_id)
            reqs.ensure_one()
        except Exception as exc:
            return {
                'error': _("Access denied"),
                'debug': ustr(exc),
            }

        if not reqs.can_change_request_text:
            return {
                'error': _("Access denied"),
            }

        try:
            reqs.request_text = request_text
        except Exception as exc:
            return {
                'error': _("Access denied"),
                'debug': ustr(exc),
            }

        return {
            'request_text': reqs.request_text,
        }

    @http.route('/crnd_wsd/api/request/do-action', type='json',
                auth='user', methods=['POST'], website=True)
    def wsd_request_actions(self, request_id, action_id, response_text=None):
        try:
            reqs = self._id_to_record('request.request', request_id)
            reqs.ensure_one()

            action_route = request.env['request.stage.route'].search([
                ('website_published', '=', True),
                ('stage_from_id', '=', reqs.sudo().stage_id.id),
                ('request_type_id', '=', reqs.sudo().type_id.id),
                ('id', '=', int(action_id)),
            ])
            action_route.ensure_one()
            action_route.check_access_rights('read')
            action_route.check_access_rule('read')
        except Exception as exc:
            return {
                'error': _("Access denied"),
                'debug': ustr(exc),
            }

        try:
            if (action_route.close and
                    action_route.require_response and response_text):
                reqs.response_text = response_text
            reqs.stage_id = action_route.stage_to_id
        except Exception as exc:
            return {
                'error': _("Access denied"),
                'debug': ustr(exc),
            }

        return {
            'status': 'ok',
            'extra_action': action_route.website_extra_action,
        }

import logging
from odoo.tests import (
    HOST,
    PORT,
)
from odoo.tools.misc import mute_logger
from odoo.addons.generic_request.tests.common import disable_mail_auto_delete
from .phantom_common import TestPhantomTour

_logger = logging.getLogger(__name__)


class TestRequestPortalMail(TestPhantomTour):
    """ Test that links in mail notifications lead portal users to website
        interface.
    """

    def setUp(self):
        super(TestRequestPortalMail, self).setUp()
        self.wsd_user = self.env.ref('crnd_wsd.user_demo_service_desk_website')
        self.request_demo_user = self.env.ref(
            'generic_request.user_demo_request')
        self.base_url = "http://%s:%s" % (HOST, PORT)

    @mute_logger('odoo.addons.mail.models.mail_mail',
                 'requests.packages.urllib3.connectionpool',
                 'odoo.models.unlink')
    def test_assign_portal(self):
        with self.phantom_env as env:
            request = env['request.request'].with_context(
                mail_create_nolog=True,
                mail_notrack=True,
            ).create({
                'type_id': env.ref('generic_request.request_type_simple').id,
                'request_text': 'Test',
            })
            with disable_mail_auto_delete(env):
                request.with_context(
                    mail_notrack=False,
                ).write({
                    'user_id': self.wsd_user.id,
                })

            assign_messages = env['mail.mail'].search([
                ('model', '=', 'request.request'),
                ('res_id', '=', request.id),
                ('body_html', 'ilike',
                 '%%/mail/view/request/%s%%' % request.id),
            ])
            self.assertEqual(len(assign_messages), 1)

        self.authenticate(self.wsd_user.login, 'demo-sd-website')
        res = self.url_open('/mail/view/request/%s' % request.id)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.url, '%s%s' % (self.base_url, request.access_url))

    @mute_logger('odoo.addons.mail.models.mail_mail')
    def test_assign_portal_no_logged_in(self):
        with self.phantom_env as env:
            request = env['request.request'].with_context(
                mail_create_nolog=True,
                mail_notrack=True,
            ).create({
                'type_id': env.ref('generic_request.request_type_simple').id,
                'request_text': 'Test',
            })
            with disable_mail_auto_delete(env):
                request.with_context(
                    mail_notrack=False,
                ).write({
                    'user_id': self.wsd_user.id,
                })

            assign_messages = env['mail.mail'].search([
                ('model', '=', 'request.request'),
                ('res_id', '=', request.id),
                ('body_html', 'ilike',
                 '%%/mail/view/request/%s%%' % request.id),
            ])
            self.assertEqual(len(assign_messages), 1)

        self._test_phantom_tour(
            '/mail/view/request/%s' % request.id,
            'crnd_wsd_tour_request_mail_login_portal')

    def test_view_on_website_button(self):
        request = self.env.ref(
            'crnd_wsd.demo_request_request_generic_question_1')
        action_res = request.action_show_on_website()
        self.assertEqual(action_res['type'], 'ir.actions.act_url')
        self.assertEqual(
            action_res['url'], '/requests/request/%s' % request.id)

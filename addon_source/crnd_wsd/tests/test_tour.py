from odoo import exceptions, tools
from odoo.tests.common import post_install, at_install
from .phantom_common import TestPhantomTour


@post_install(True)
@at_install(False)
class TestWebsiteServiceDesk(TestPhantomTour):

    def setUp(self):
        super(TestWebsiteServiceDesk, self).setUp()
        self.user_demo = self.env.ref(
            'crnd_wsd.user_demo_service_desk_website')
        self.group_portal = self.env.ref('base.group_portal')

    def test_tour_request_base(self):
        self.assertIn(self.group_portal, self.user_demo.groups_id)
        self._test_phantom_tour(
            '/', 'crnd_wsd_tour_request_base',
            login=self.user_demo.login)

    def test_tour_request_actions_ok(self):
        self.assertIn(self.group_portal, self.user_demo.groups_id)

        with self.phantom_env as env:
            env.ref(
                'crnd_wsd.request_stage_route_type_generic_sent_to_closed'
            ).write({
                'website_published': True,
                'require_response': True,
            })

        self._test_phantom_tour(
            '/', 'crnd_wsd_tour_request_actions_ok',
            login=self.user_demo.login)

    def test_tour_request_actions_redirect(self):
        self.assertIn(self.group_portal, self.user_demo.groups_id)

        with self.phantom_env as env:
            env.ref(
                'crnd_wsd.request_stage_route_type_generic_sent_to_closed'
            ).write({
                'website_published': True,
                'require_response': False,
                'website_extra_action': 'redirect_to_my',
            })

        self._test_phantom_tour(
            '/', 'crnd_wsd_tour_request_actions_redirect',
            login=self.user_demo.login)

    def test_tour_request_actions_not_allowed(self):
        self.assertIn(self.group_portal, self.user_demo.groups_id)

        with self.phantom_env as env:
            req_send = env.ref(
                'crnd_wsd.request_stage_route_type_generic_draft_to_sent')
            req_send.allowed_user_ids = env.ref('base.user_root')

        self._test_phantom_tour(
            '/', 'crnd_wsd_tour_request_actions_not_allowed',
            login=self.user_demo.login)

    @tools.mute_logger('odoo.addons.crnd_wsd.controllers.main')
    def test_tour_request_new(self):
        self.assertIn(self.group_portal, self.user_demo.groups_id)

        # Patch create method
        def monkey_create(self, vals):
            # pylint: disable=translation-required
            if vals.get('request_text', '') == '<p>create_user_error</p>':
                raise exceptions.UserError('Test user_error')
            if vals.get('request_text', '') == '<p>create_error</p>':
                raise Exception('Test exception')
            return monkey_create.origin(self, vals)
        self.env['request.request']._patch_method('create', monkey_create)

        new_requests = self._test_phantom_tour_requests(
            '/', 'crnd_wsd_tour_request_new',
            login=self.user_demo.login)

        # Revert patched method
        self.env['request.request']._revert_method('create')

        self.assertEqual(len(new_requests), 1)
        self.assertTrue(
            new_requests.request_text.startswith(
                u'<h1>Test generic request (modified)</h1>'))

    def test_tour_request_new_default_text(self):
        with self.phantom_env as env:
            env.ref(
                'crnd_wsd.request_type_generic'
            ).write({
                'default_request_text': 'Default text',
            })
        self._test_phantom_tour(
            '/', 'crnd_wsd_tour_request_new_default_text',
            login=self.user_demo.login)

    def test_tour_public_user(self):
        with self.phantom_env as env:
            env.user.company_id.request_wsd_public_ui_visibility = 'restrict'
        self._test_phantom_tour(
            '/', 'crnd_wsd_tour_request_public_user')

    def test_tour_public_user_redirect(self):
        with self.phantom_env as env:
            env.user.company_id.request_wsd_public_ui_visibility = 'redirect'
        self._test_phantom_tour(
            '/', 'crnd_wsd_tour_request_public_user_redirect')

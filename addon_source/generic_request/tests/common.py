import logging
from contextlib import contextmanager
from odoo.tests.common import SavepointCase
from odoo.addons.generic_mixin.tests.common import (
    ReduceLoggingMixin,
    AccessRulesFixMixinST,
)


try:
    # pylint: disable=unused-import
    from freezegun import freeze_time  # noqa
except ImportError:  # pragma: no cover
    logging.getLogger(__name__).warning(
        "freezegun not installed. Tests will not work!")


@contextmanager
def disable_mail_auto_delete(env):
    def patched_method(self, vals):
        vals = dict(vals, auto_delete=False)
        return patched_method.origin(self, vals)
    env['mail.mail']._patch_method(
        'create', patched_method)

    yield

    env['mail.mail']._revert_method('create')


class RequestCase(AccessRulesFixMixinST,
                  ReduceLoggingMixin,
                  SavepointCase):
    """ BAse tests case for tests related to generic request
    """

    @classmethod
    def setUpClass(cls):
        super(RequestCase, cls).setUpClass()
        cls.general_category = cls.env.ref(
            'generic_request.request_category_demo_general')
        cls.resource_category = cls.env.ref(
            'generic_request.request_category_demo_resource')
        cls.tec_configuration_category = cls.env.ref(
            'generic_request.request_category_demo_technical_configuration')

        # Request type
        cls.simple_type = cls.env.ref('generic_request.request_type_simple')
        cls.sequence_type = cls.env.ref(
            'generic_request.request_type_sequence')
        cls.non_ascii_type = cls.env.ref(
            'generic_request.request_type_non_ascii')
        cls.access_type = cls.env.ref(
            'generic_request.request_type_access')

        # Stages
        cls.stage_draft = cls.env.ref(
            'generic_request.request_stage_type_simple_draft')
        cls.stage_sent = cls.env.ref(
            'generic_request.request_stage_type_simple_sent')
        cls.stage_confirmed = cls.env.ref(
            'generic_request.request_stage_type_simple_confirmed')
        cls.stage_rejected = cls.env.ref(
            'generic_request.request_stage_type_simple_rejected')
        cls.stage_new = cls.env.ref(
            'generic_request.request_stage_type_sequence_new')
        # Routes
        cls.route_draft_to_sent = cls.env.ref(
            'generic_request.request_stage_route_type_simple_draft_to_sent')
        cls.non_ascii_route_draft_to_sent = cls.env.ref(
            'generic_request.request_stage_route_type_non_ascii_draft_to_sent')

        # Requests
        cls.request_1 = cls.env.ref(
            'generic_request.request_request_type_simple_demo_1')
        cls.request_2 = cls.env.ref(
            'generic_request.request_request_type_access_demo_1')

        # Users
        cls.demo_user = cls.env.ref('base.user_demo')
        cls.request_user = cls.env.ref(
            'generic_request.user_demo_request')
        cls.request_manager = cls.env.ref(
            'generic_request.user_demo_request_manager')
        cls.request_manager_2 = cls.env.ref(
            'generic_request.user_demo_request_manager_2')

    def _close_request(self, request, stage, response_text=False, user=None):
        if user is None:
            user = self.env.user

        close_route = self.env['request.stage.route'].with_user(user).search([
            ('request_type_id', '=', request.type_id.id),
            ('stage_to_id', '=', stage.id),
        ])
        close_route.ensure_one()
        wiz = self.env['request.wizard.close'].with_user(user).create({
            'request_id': request.id,
            'close_route_id': close_route.id,
            'response_text': response_text,
        })
        wiz.action_close_request()

        self.assertEqual(request.stage_id, stage)
        self.assertEqual(request.response_text, response_text)


class AccessRightsCase(AccessRulesFixMixinST,
                       ReduceLoggingMixin,
                       SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(AccessRightsCase, cls).setUpClass()
        cls.simple_type = cls.env.ref('generic_request.request_type_simple')

        # Users
        cls.demo_user = cls.env.ref('generic_request.user_demo_request')
        cls.demo_manager = cls.env.ref(
            'generic_request.user_demo_request_manager')

        # Envs
        cls.uenv = cls.env(user=cls.demo_user)
        cls.menv = cls.env(user=cls.demo_manager)

        # Request Type
        cls.usimple_type = cls.uenv.ref('generic_request.request_type_simple')
        cls.msimple_type = cls.menv.ref('generic_request.request_type_simple')

        # Request category
        cls.ucategory_demo_general = cls.uenv.ref(
            'generic_request.request_category_demo_general')
        cls.mcategory_demo_general = cls.menv.ref(
            'generic_request.request_category_demo_general')

        # Request view action
        cls.request_action = cls.env.ref(
            'generic_request.action_request_window')

    def _read_request_fields(self, user, request):
        fields = list(
            self.env['request.request'].with_user(
                user
            ).load_views(
                self.request_action.views
            )['fields_views']['form']['fields']
        )
        return request.with_user(user).read(fields)

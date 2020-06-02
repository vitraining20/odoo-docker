from .common import RequestCase


class TestRequestBase(RequestCase):

    def setUp(self):
        super(TestRequestBase, self).setUp()
        self.Request = self.env['request.request']

    def test_default_request_text(self):

        request = self.Request.new({
            'type_id': self.access_type.id,
            'category_id': self.tec_configuration_category.id,
            'user_id': self.request_manager.id,
        })
        self.assertFalse(request.request_text)

        request.onchange_type_id()

        self.assertEqual(request.request_text,
                         request.type_id.default_request_text)

    def test_default_response_text(self):
        request = self.request_2

        close_route = self.env.ref(
            'generic_request.request_stage_route_type_access_sent_to_rejected')
        close_stage = self.env.ref(
            'generic_request.request_stage_route_type_access_sent_to_rejected')

        request.stage_id = close_stage.id

        request_closing = self.env['request.wizard.close'].create({
            'request_id': request.id,
            'close_route_id': close_route.id,
        })
        self.assertFalse(request_closing.response_text)

        request_closing.onchange_close_route_id()

        self.assertEqual(request_closing.response_text,
                         close_route.default_response_text)

        request_closing.action_close_request()

        self.assertTrue(request.closed)

        self.assertEqual(request.response_text,
                         close_route.default_response_text)

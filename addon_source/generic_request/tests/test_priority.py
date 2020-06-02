from odoo.tests.common import SavepointCase
from odoo.addons.generic_mixin.tests.common import ReduceLoggingMixin


class TestPriority(ReduceLoggingMixin, SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestPriority, cls).setUpClass()
        cls.test_request_type = cls.env.ref(
            'generic_request.request_type_with_complex_priority')
        cls.test_request = cls.env.ref(
            'generic_request.demo_request_with_complex_priority')

    def test_complex_priority(self):
        # test complex priority
        self.assertEqual(self.test_request.priority, '2')

        # change impact and urgency
        self.test_request.impact = '0'
        self.test_request.urgency = '1'

        # test complex priority calculation
        self.assertEqual(self.test_request.priority, '1')

        event = self.env['request.event'].search(
            [('request_id', '=', self.test_request.id)])
        self.assertEqual(event[0].event_code, 'urgency-changed')
        self.assertEqual(event[1].event_code, 'priority-changed')
        self.assertEqual(event[2].event_code, 'impact-changed')
        self.assertEqual(event[3].event_code, 'priority-changed')

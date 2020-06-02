from odoo.tests import common
from odoo.addons.generic_mixin.tests.common import ReduceLoggingMixin


class RequestKindCase(ReduceLoggingMixin, common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(RequestKindCase, cls).setUpClass()

        cls.request_kind = cls.env.ref('generic_request.request_kind_demo')

    def test_menuitem_toggle(self):
        self.assertFalse(self.request_kind.menuitem_toggle)
        self.assertFalse(self.request_kind.menuitem_name)
        self.assertFalse(self.request_kind.menuaction_name)

        # toggle (enable) menuitem button
        self.request_kind.menuitem_toggle = True

        self.assertTrue(self.request_kind.menuitem_id)
        self.assertTrue(self.request_kind.menuaction_id)
        self.assertEqual(
            self.request_kind.menuitem_name, self.request_kind.name
        )
        self.assertEqual(
            self.request_kind.menuaction_name, self.request_kind.name
        )

        # toggle (disable) menuitem button
        self.request_kind.menuitem_toggle = False

        action = self.request_kind.menuaction_id

        self.assertFalse(self.request_kind.menuitem_id)
        self.assertFalse(self.request_kind.menuaction_id)

        self.assertFalse(action.exists())

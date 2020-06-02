from odoo.exceptions import (AccessError,
                             UserError)
from .common import RequestCase


class TestRequestSimpleFlow(RequestCase):
    """Test request Simple Flow
    """

    def test_090_simple_flow_assign_self(self):
        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)
        self.assertFalse(self.request_1.date_assigned)
        self.assertFalse(self.request_1.user_id)

        # Assign request to request manager
        manager = self.request_manager

        # If no user specified for wizard, current user will be automaticaly
        # selected
        AssignWizard = self.env['request.wizard.assign']
        assign_wizard = AssignWizard.with_user(manager).create({
            'request_id': self.request_1.id,
        })
        self.assertEqual(assign_wizard.user_id, manager)

        assign_wizard.do_assign()
        self.assertEqual(self.request_1.user_id, manager)
        self.assertTrue(self.request_1.date_assigned)

        # Undo assign request
        manager = self.request_manager
        self.request_1.with_user(manager).write({'user_id': False})
        self.assertFalse(self.request_1.user_id)
        self.assertFalse(self.request_1.date_assigned)

    def test_093_simple_flow_assign_self_with_comment(self):
        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)
        self.assertFalse(self.request_1.date_assigned)
        self.assertFalse(self.request_1.user_id)

        # Assign request to request manager
        manager = self.request_manager

        # If no user specified for wizard, current user will be automaticaly
        # selected
        AssignWizard = self.env['request.wizard.assign']
        assign_wizard = AssignWizard.with_user(manager).create({
            'request_id': self.request_1.id,
            'comment': 'Test Comment',
        })
        self.assertEqual(assign_wizard.user_id, manager)

        assign_wizard.do_assign()
        self.assertEqual(self.request_1.user_id, manager)
        self.assertTrue(self.request_1.date_assigned)
        self.assertTrue(self.env['mail.message'].search_count([
            ('model', '=', 'request.request'),
            ('res_id', '=', self.request_1.id),
            ('body', 'ilike', 'Test Comment'),
            ('subtype_id', '=', self.env.ref('mail.mt_note').id),
        ]))

    def test_098_simple_flow_assign_self_assign_to_me(self):
        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)
        self.assertFalse(self.request_1.date_assigned)
        self.assertFalse(self.request_1.user_id)

        # Assign request to request manager
        manager = self.request_manager

        # If no user specified for wizard, current user will be automaticaly
        # selected
        self.request_1.with_user(manager).action_request_assign_to_me()
        self.assertEqual(self.request_1.user_id, manager)
        self.assertTrue(self.request_1.date_assigned)

    def test_100_simple_flow_su_confirm(self):

        self.assertEqual(self.request_1.stage_id, self.stage_draft)
        self.assertFalse(self.request_1.can_be_closed)

        # Make request sent
        self.request_1.write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)
        self.assertTrue(self.request_1.can_be_closed)

        # Make request confirmed
        self._close_request(self.request_1, self.stage_confirmed)
        self.assertFalse(self.request_1.can_be_closed)

    def test_110_simple_flow_su_reject(self):

        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)

        # Make request rejected
        with self.assertRaises(UserError):
            # No response text provided, but it is required
            self._close_request(self.request_1, self.stage_rejected)

        self._close_request(
            self.request_1, self.stage_rejected,
            response_text='<p>Rejected!</p>')

    def test_120_simple_flow_access_confirm_access_error(self):
        user = self.request_user

        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.with_user(user).write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)

        # Make request confirmed
        with self.assertRaises(AccessError):
            self._close_request(
                self.request_1, self.stage_confirmed, user=user)

    def test_130_simple_flow_access_confirm_access_ok(self):
        user = self.request_user
        manager = self.request_manager

        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.with_user(user).write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)
        self.assertFalse(self.request_1.date_closed)
        self.assertFalse(self.request_1.closed_by_id)

        # Make request confirmed (manager belongs to group that allowed to
        # confirm requests)
        self._close_request(self.request_1, self.stage_confirmed, user=manager)
        self.assertTrue(self.request_1.date_closed)
        self.assertEqual(self.request_1.closed_by_id, manager)

    def test_140_simple_flow_access_reject_access_error_user_1(self):
        user = self.request_user

        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.with_user(user).write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)

        # Make request confirmed
        # (User cannot reject request)
        with self.assertRaises(AccessError):
            self.request_1.with_user(user).write(
                {'stage_id': self.stage_rejected.id})

    def test_145_simple_flow_access_reject_access_error_user_2(self):
        user = self.request_user
        manager = self.request_manager

        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.with_user(user).write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)

        # Make request reject
        # (Manager alson cannot reject request)
        with self.assertRaises(AccessError):
            self.request_1.with_user(manager).write(
                {'stage_id': self.stage_rejected.id})

    def test_150_simple_flow_access_reject_access_ok(self):
        user = self.request_user
        manager_2 = self.request_manager_2

        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.with_user(user).write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)
        self.assertFalse(self.request_1.date_closed)
        self.assertFalse(self.request_1.closed_by_id)

        # Make request rejected
        # Manager 2 can do it, because it is in list of allowed users for
        # this route
        self.request_1.with_user(manager_2).write(
            {'stage_id': self.stage_rejected.id})
        self.assertEqual(self.request_1.stage_id, self.stage_rejected)
        self.assertTrue(self.request_1.date_closed)
        self.assertEqual(self.request_1.closed_by_id, manager_2)

    def test_155_simple_flow_circle(self):
        # draft -> sent -> rejected -> draft
        user = self.request_user
        manager_2 = self.request_manager_2

        self.assertEqual(self.request_1.stage_id, self.stage_draft)

        # Make request sent
        self.request_1.with_user(user).write({'stage_id': self.stage_sent.id})
        self.assertEqual(self.request_1.stage_id, self.stage_sent)
        self.assertFalse(self.request_1.date_closed)
        self.assertFalse(self.request_1.closed_by_id)

        # Make request rejected
        self.request_1.with_user(manager_2).write(
            {'stage_id': self.stage_rejected.id})
        self.assertEqual(self.request_1.stage_id, self.stage_rejected)
        self.assertTrue(self.request_1.date_closed)
        self.assertEqual(self.request_1.closed_by_id, manager_2)

        # Go to draft state again
        self.request_1.with_user(user).write({'stage_id': self.stage_draft.id})
        self.assertEqual(self.request_1.stage_id, self.stage_draft)
        self.assertFalse(self.request_1.closed)

    def test_160_simple_flow_assign_closed(self):
        # Closed requests cannot be reassigned.
        self.request_1.stage_id = self.stage_sent.id
        self.assertEqual(self.request_1.stage_id, self.stage_sent)

        # Make request confirmed (manager belongs to group that allowed to
        # confirm requests)
        self._close_request(self.request_1, self.stage_confirmed)
        self.assertTrue(self.request_1.date_closed)

        # Assign request to manager
        with self.assertRaises(UserError):
            self.request_1.action_request_assign()

from odoo import exceptions
from odoo.tools.misc import mute_logger
from .common import AccessRightsCase


class TestRequestAccessRights(AccessRightsCase):
    """Test request access rules
    """

    def test_090_user_request_type_access(self):
        with mute_logger('odoo.models'):
            with self.assertRaises(exceptions.AccessError):
                self.usimple_type.name   # pylint: disable=pointless-statement

        # Subscribe demo-user to 'simple request' type
        self.simple_type.message_subscribe(self.demo_user.partner_id.ids)

        # Ensure, after subscription simple_type is readable
        self.assertTrue(self.usimple_type.name)

    def test_100_user_request_access(self):
        self.simple_type.message_subscribe(self.demo_user.partner_id.ids)

        stage_draft = self.uenv.ref(
            'generic_request.request_stage_type_simple_draft')
        stage_sent = self.uenv.ref(
            'generic_request.request_stage_type_simple_sent')

        # Create request
        request = self.uenv['request.request'].create({
            'type_id': self.usimple_type.id,
            'category_id': self.ucategory_demo_general.id,
            'request_text': 'Demo'
        })
        self.assertEqual(request.stage_id, stage_draft)

        # Move request to sent stage
        request.write({'stage_id': stage_sent.id})
        self.assertEqual(request.stage_id, stage_sent)

    def test_110_manager_request_type_access(self):
        # Ensure, simple_type is readable for manager
        self.assertTrue(self.msimple_type.name)

    def test_120_manager_request_access(self):
        stage_draft = self.menv.ref(
            'generic_request.request_stage_type_simple_draft')
        stage_sent = self.menv.ref(
            'generic_request.request_stage_type_simple_sent')

        # Create request
        request = self.menv['request.request'].create({
            'type_id': self.msimple_type.id,
            'category_id': self.mcategory_demo_general.id,
            'request_text': 'Demo'
        })
        self.assertEqual(request.stage_id, stage_draft)

        # Move request to sent stage
        request.write({'stage_id': stage_sent.id})
        self.assertEqual(request.stage_id, stage_sent)

    def test_130_user_sent_request_manager_confirm(self):
        self.simple_type.message_subscribe(self.demo_user.partner_id.ids)

        # Create request
        request = self.uenv['request.request'].create({
            'type_id': self.usimple_type.id,
            'category_id': self.ucategory_demo_general.id,
            'request_text': 'Demo'
        })

        # Move request to sent stage
        request.write({
            'stage_id': self.uenv.ref(
                'generic_request.request_stage_type_simple_sent').id,
        })
        self.assertEqual(
            request.stage_id,
            self.uenv.ref('generic_request.request_stage_type_simple_sent'))

        # Manager read request
        mrequest = self.menv['request.request'].browse(request.id)

        mrequest.write({
            'stage_id': self.menv.ref(
                'generic_request.request_stage_type_simple_confirmed').id,
        })
        self.assertEqual(
            mrequest.stage_id,
            self.menv.ref(
                'generic_request.request_stage_type_simple_confirmed'))

    def test_140_access_request_read(self):
        request = self.menv['request.request'].create({
            'type_id': self.msimple_type.id,
            'category_id': self.mcategory_demo_general.id,
            'request_text': 'Demo'
        })
        request.message_subscribe(self.demo_user.partner_id.ids)
        self._read_request_fields(self.demo_user, request)

    def test_150_access_request_read_write_unlink_denied(self):
        request = self.menv['request.request'].create({
            'type_id': self.msimple_type.id,
            'category_id': self.mcategory_demo_general.id,
            'request_text': 'Demo'
        })

        with mute_logger('odoo.models'):
            with self.assertRaises(exceptions.AccessError):
                with self.env.cr.savepoint():
                    self._read_request_fields(self.demo_user, request)

            with self.assertRaises(exceptions.AccessError):
                with self.env.cr.savepoint():
                    request.with_user(self.demo_user).write({
                        'request_text': 'Test',
                    })

            with self.assertRaises(exceptions.AccessError):
                with self.env.cr.savepoint():
                    request.with_user(self.demo_user).unlink()

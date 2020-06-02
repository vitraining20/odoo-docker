from .common import RequestCase


class TestRequestAuthor(RequestCase):
    def setUp(self):
        super(TestRequestAuthor, self).setUp()
        self.author_default = self.env.ref('base.partner_root')
        self.partner_default = False
        self.author1 = self.env.ref('base.res_partner_address_2')
        self.partner1 = self.env.ref('base.res_partner_1')
        self.group = 'generic_request.group_request_user_can_change_author'
        self.group_change_author = self.env.ref(self.group)

    def test_request_author_on_change(self):
        request = self.env['request.request'].new({
            'type_id': self.simple_type.id,
            'category_id': self.general_category.id,
            'stage_id': self.stage_draft.id,
            'author_id': self.author_default.id,
            'request_text': 'Test request',
        })

        self.assertEqual(request.stage_id.id, self.stage_draft.id)
        self.assertEqual(request.author_id.id, self.author_default.id)
        self.assertEqual(request.partner_id.id, self.partner_default)

        request.author_id = self.author1.id
        request._onchange_author_id()
        self.assertEqual(request.author_id.id, self.author1.id)
        self.assertEqual(request.partner_id.id, self.partner1.id)

    def test_can_change_author(self):
        request = self.env['request.request'].with_user(
            self.request_manager).create({
                'type_id': self.simple_type.id,
                'category_id': self.general_category.id,
                'request_text': 'Test request'})

        self.assertEqual(self.request_manager.has_group(self.group), False)

        self.assertEqual(request.stage_id.id, self.stage_draft.id)
        self.assertEqual(request.can_change_author, False)

        self.request_manager.groups_id += self.group_change_author
        self.assertEqual(self.request_manager.has_group(self.group), True)
        self.assertEqual(request.can_change_author, True)

        request.stage_id = self.stage_sent
        self.assertEqual(request.stage_id.id, self.stage_sent.id)
        self.assertEqual(request.can_change_author, False)

    def test_author_compute(self):
        partner = self.env.ref('base.res_partner_3')
        author = self.env.ref('base.res_partner_address_5')

        self.assertFalse(partner.request_ids)
        self.assertEqual(partner.request_count, 0)
        self.assertFalse(author.request_ids)
        self.assertEqual(author.request_count, 0)

        request = self.env['request.request'].create({
            'type_id': self.simple_type.id,
            'category_id': self.general_category.id,
            'request_text': 'Test request',
            'partner_id': partner.id,
        })
        self.assertTrue(partner.request_ids)
        self.assertEqual(partner.request_count, 1)
        self.assertFalse(author.request_ids)
        self.assertEqual(author.request_count, 0)
        self.assertNotIn(author, request.message_partner_ids)
        self.assertNotIn(partner, request.message_partner_ids)

        request = self.env['request.request'].create({
            'type_id': self.simple_type.id,
            'category_id': self.general_category.id,
            'request_text': 'Test request',
            'author_id': partner.id,
            'partner_id': False,
        })
        self.assertTrue(partner.request_ids)
        self.assertEqual(partner.request_count, 2)
        self.assertFalse(author.request_ids)
        self.assertEqual(author.request_count, 0)
        self.assertNotIn(author, request.message_partner_ids)
        self.assertIn(partner, request.message_partner_ids)

        request = self.env['request.request'].create({
            'type_id': self.simple_type.id,
            'category_id': self.general_category.id,
            'request_text': 'Test request',
            'author_id': author.id,
        })
        self.assertTrue(partner.request_ids)
        self.assertEqual(partner.request_count, 3)
        self.assertTrue(author.request_ids)
        self.assertEqual(author.request_count, 1)
        self.assertIn(author, request.message_partner_ids)
        self.assertNotIn(partner, request.message_partner_ids)

        request = self.env['request.request'].create({
            'type_id': self.simple_type.id,
            'category_id': self.general_category.id,
            'request_text': 'Test request',
            'author_id': author.id,
            'partner_id': False,
        })
        self.assertTrue(partner.request_ids)
        self.assertEqual(partner.request_count, 3)
        self.assertTrue(author.request_ids)
        self.assertEqual(author.request_count, 2)
        self.assertIn(author, request.message_partner_ids)
        self.assertNotIn(partner, request.message_partner_ids)

        request.author_id = partner
        self.assertIn(author, request.message_partner_ids)
        self.assertIn(partner, request.message_partner_ids)

        # Test actions
        act = partner.action_show_related_requests()
        self.assertEqual(
            self.env[act['res_model']].search(act['domain']),
            partner.request_ids)
        act = author.action_show_related_requests()
        self.assertEqual(
            self.env[act['res_model']].search(act['domain']),
            author.request_ids)
        req = self.env['request.request'].with_context(
            dict(act['context'])).create({
                'type_id': self.simple_type.id,
                'request_text': 'Test',
            })
        self.assertEqual(req.partner_id, partner)
        self.assertEqual(req.author_id, author)

    def test_compute_partner_of_demo_request(self):
        self.assertEqual(
            self.env.ref(
                'generic_request.request_request_type_sequence_demo_1'
            ).partner_id,
            self.env.ref('base.res_partner_2'))

from odoo import models, fields, api
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    request_by_partner_ids = fields.One2many(
        'request.request', 'partner_id',
        readonly=True, copy=False)
    request_by_author_ids = fields.One2many(
        'request.request', 'author_id',
        readonly=True, copy=False)
    request_ids = fields.Many2many(
        'request.request',
        'request_request_partner_author_rel',
        'partner_id', 'request_id',
        readonly=True, copy=False, store=True,
        compute='_compute_request_data')
    request_count = fields.Integer(
        'Requests', compute='_compute_request_data',
        store=True, readonly=True)

    @api.depends('request_by_partner_ids', 'request_by_author_ids')
    def _compute_request_data(self):
        for record in self:
            record.request_ids = (
                record.request_by_partner_ids + record.request_by_author_ids)
            record.request_count = len(record.request_ids)

    def action_show_related_requests(self):
        self.ensure_one()
        action = self.env.ref(
            'generic_request.action_request_window').read()[0]
        action.update({
            'domain': expression.OR([
                [('partner_id', 'in', self.ids)],
                [('author_id', 'in', self.ids)],
            ]),
            'context': dict(
                self.env.context,
                default_partner_id=self.commercial_partner_id.id,
                default_author_id=self.id,
            ),
        })
        return action

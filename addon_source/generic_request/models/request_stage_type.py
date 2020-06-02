from odoo import models, fields, api
from .request_stage import DEFAULT_BG_COLOR, DEFAULT_LABEL_COLOR


class RequestStageType(models.Model):
    _name = 'request.stage.type'
    _inherit = [
        'generic.mixin.name_with_code',
        'generic.mixin.uniq_name_code',
    ]
    _description = 'Request Stage Type'

    # Defined in generic.mixin.name_with_code
    name = fields.Char()
    code = fields.Char()

    active = fields.Boolean(index=True, default=True)

    bg_color = fields.Char(default=DEFAULT_BG_COLOR, string="Backgroung Color")
    label_color = fields.Char(default=DEFAULT_LABEL_COLOR)
    request_ids = fields.One2many('request.request', 'stage_type_id')
    request_count = fields.Integer(
        compute='_compute_request_count', readonly=True)

    @api.depends('request_ids')
    def _compute_request_count(self):
        for rec in self:
            rec.request_count = len(rec.request_ids)

    def action_show_requests(self):
        self.ensure_one()
        action = self.env.ref(
            'generic_request.action_request_window').read()[0]
        ctx = dict(self.env.context)
        ctx.update({
            'default_stage_type_id': self.id,
        })
        return dict(
            action,
            context=ctx,
            domain=[('stage_type_id', '=', self.id)]
        )

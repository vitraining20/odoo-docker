from odoo import models, fields


class RequestWizardAssign(models.TransientModel):
    _name = 'request.wizard.assign'
    _description = 'Request Wizard: Assign'

    def _default_user_id(self):
        return self.env.user

    request_id = fields.Many2one('request.request', 'Request', requeired=True)
    user_id = fields.Many2one(
        'res.users', string="User", default=_default_user_id, required=True)
    partner_id = fields.Many2one(
        'res.partner', related="user_id.partner_id",
        readonly=True, store=False)
    comment = fields.Text()

    def do_assign(self):
        for rec in self:
            rec.request_id.ensure_can_assign()
            rec.request_id.user_id = rec.user_id
            if rec.comment:
                rec.request_id.message_post(body=rec.comment)

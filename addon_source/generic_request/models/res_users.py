from odoo import models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def action_show_related_requests(self):
        return self.partner_id.action_show_related_requests()

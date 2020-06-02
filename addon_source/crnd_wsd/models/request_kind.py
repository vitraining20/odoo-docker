from odoo import models, fields


class RequestKind(models.Model):
    _inherit = "request.kind"

    show_as_website_filter = fields.Boolean(default=False, index=True)
    website_filter_name = fields.Char(index=True, translate=True)

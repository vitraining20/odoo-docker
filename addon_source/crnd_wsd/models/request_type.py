from odoo import models, fields


class RequestType(models.Model):
    _inherit = "request.type"

    website_comments_closed = fields.Boolean(
        'Are comments not available?', default=False,
        help="Disable website comments on closed requests")

    # Request type has no websitepublish url yet, so we just need
    # website_published field, thus implement it in explicit way here insetead
    # of inheriting from "website.published.mixin"
    website_published = fields.Boolean('Visible in Website', copy=False)

    def website_publish_button(self):
        for rec in self:
            rec.website_published = not rec.website_published

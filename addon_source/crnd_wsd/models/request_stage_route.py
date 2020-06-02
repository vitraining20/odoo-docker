from odoo import models, fields


class RequestStageRoute(models.Model):
    _inherit = "request.stage.route"

    # Request stage route has no websitepublish url yet, so we just need
    # website_published field, thus implement it in explicit way here insetead
    # of inheriting from "website.published.mixin"
    website_published = fields.Boolean('Visible in Website', copy=False)
    website_button_style = fields.Selection([
        ('default', 'Default'),
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('info', 'Info'),
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('link', 'Link'),
    ], default='default', help='Buttons style for website')
    website_extra_action = fields.Selection(
        [('redirect_to_my', 'Redirect to My Requests')])

    def website_publish_button(self):
        for rec in self:
            rec.website_published = not rec.website_published
        return True

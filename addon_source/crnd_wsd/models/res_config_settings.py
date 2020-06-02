from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    request_wsd_public_ui_visibility = fields.Selection(
        related='company_id.request_wsd_public_ui_visibility',
        readonly=False,
        string='Website Service Desk (Public Visibility)',
        help="""Redirect to login - unauthorized users will be
         automatically redirected to login page.
         Restricted UI - unauthorized users will be able to pass
         all steps of creating a request but unable to submit
         request until logged in."""
        )

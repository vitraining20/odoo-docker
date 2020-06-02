from odoo import models, fields, api, exceptions, _


class RequestWizardClose(models.TransientModel):
    _name = 'request.wizard.close'
    _description = 'Request Wizard: Close'

    request_id = fields.Many2one('request.request', 'Request', requeired=True)
    close_route_id = fields.Many2one(
        'request.stage.route', 'Close as', required=True)
    require_response = fields.Boolean(
        related="close_route_id.require_response", readonly=True)
    response_text = fields.Html('Response')

    def _get_next_route_domain(self):
        self.ensure_one()
        return [
            ('close', '=', True),
            ('stage_from_id', '=', self.request_id.stage_id.id),
        ]

    @api.onchange('request_id')
    def onchange_request_id(self):
        if self.request_id:
            self.response_text = self.request_id.response_text
            self.close_route_id = self.env['request.stage.route'].search(
                self._get_next_route_domain(), limit=1)
            return {
                'domain': {
                    'close_route_id': self._get_next_route_domain(),
                },
            }
        return {}

    @api.onchange('close_route_id')
    def onchange_close_route_id(self):
        for rec in self:
            rec.response_text = rec.close_route_id.default_response_text

    def action_close_request(self):
        self.ensure_one()

        if self.response_text == '<p><br></p>':
            self.response_text = False

        if self.require_response and not self.response_text:
            raise exceptions.UserError(_("Response text is required!"))

        # Set response_text here, because it may be used in conditions
        # that checks if it is allowed to move request by specified route
        self.request_id.response_text = self.response_text
        self.request_id.stage_id = self.close_route_id.stage_to_id

from odoo import models, fields, api, _
from odoo.exceptions import (ValidationError,
                             AccessError)


class RequestStageRoute(models.Model):
    _name = "request.stage.route"
    _inherit = [
        'mail.thread',
    ]
    _description = "Request Stage Route"
    _order = "sequence"

    name = fields.Char(readonly=False, translate=True)
    sequence = fields.Integer(
        default=5, index=True, required=True, track_visibility='onchange')
    stage_from_id = fields.Many2one(
        'request.stage', 'From', ondelete='restrict',
        required=True, index=True, track_visibility='onchange')
    stage_to_id = fields.Many2one(
        'request.stage', 'To', ondelete='restrict',
        required=True, index=True, track_visibility='onchange')
    request_type_id = fields.Many2one(
        'request.type', 'Request Type', ondelete='cascade',
        required=True, index=True, track_visibility='onchange')

    allowed_group_ids = fields.Many2many(
        'res.groups', string='Allowed groups')
    allowed_user_ids = fields.Many2many(
        'res.users', string='Allowed users')
    close = fields.Boolean(
        related='stage_to_id.closed', store=True, index=True, readonly=True,
        help='If set, then this route will close request')

    require_response = fields.Boolean(
        store=True,
        help="If set, then user will be asked for comment on this route")
    default_response_text = fields.Html(translate=True)

    _sql_constraints = [
        ('stage_stage_from_to_type_uniq',
         'UNIQUE (request_type_id, stage_from_id, stage_to_id)',
         'Such route already present in this request type')
    ]

    def name_get(self):
        res = []
        for record in self:
            name = u"%s -> %s" % (record.stage_from_id.name,
                                  record.stage_to_id.name)
            if record.name:
                name = u"%s [%s]" % (name, record.name)

            if self.env.context.get('name_only', False) and record.name:
                name = record.name

            res += [(record.id, name)]
        return res

    def _ensure_can_move(self, request):
        self.ensure_one()

        if self.env.su:
            # no access rights checks for superuser
            return

        # Access rights checks (user)
        allowed_users = self.allowed_user_ids
        if allowed_users and self.env.user not in allowed_users:
            raise AccessError(
                _(
                    "This stage change '%s' restricted by access rights.\n"
                    "Request: %s\n"
                    "Request Type: %s\n"
                    "Request Category: %s\n"
                ) % (
                    self.display_name,
                    request.sudo().display_name,
                    request.sudo().type_id.display_name,
                    request.sudo().category_id.display_name,
                )
            )

        # Access rights checks (group)
        allowed_groups = self.allowed_group_ids
        if allowed_groups and not allowed_groups & self.env.user.groups_id:
            raise AccessError(
                _(
                    "This stage change '%s' restricted by access rights.\n"
                    "Request: %s\n"
                    "Request Type: %s\n"
                    "Request Category: %s\n"
                ) % (
                    self.display_name,
                    request.sudo().display_name,
                    request.sudo().type_id.display_name,
                    request.sudo().category_id.display_name,
                )
            )

    @api.model
    def ensure_route(self, request, to_stage_id):
        """ Ensure that route to specified stage_id for this request exists
            and current user have right to use it

            :return: return route for this move
        """
        route = self.search([('request_type_id', '=', request.type_id.id),
                             ('stage_from_id', '=', request.stage_id.id),
                             ('stage_to_id', '=', to_stage_id)])
        if not route:
            RequestStage = self.env['request.stage']
            stage = RequestStage.browse(to_stage_id) if to_stage_id else None
            raise ValidationError(
                _("Cannot move request to this stage: no route.\n"
                  "\tRequest: %s\n"
                  "\tTo stage id: %s\n"
                  "\tTo stage name: %s\n"
                  "\tFrom stage name: %s\n"
                  "") % (request.name,
                         to_stage_id,
                         stage.name if stage else None,
                         request.stage_id.name if request.stage_id else None)
            )

        route._ensure_can_move(request)
        return route

    def hook_before_stage_change(self, request):
        """ Could be used outside to do some work before request stage changed
        """
        self.ensure_one()

    def hook_after_stage_change(self, request):
        """ Could be redefined, by other modules, to add mode logic
            on stage move of request
        """
        self.ensure_one()

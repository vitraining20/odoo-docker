from odoo import models, fields, api, exceptions, _


DEFAULT_BG_COLOR = 'rgba(120,120,120,1)'
DEFAULT_LABEL_COLOR = 'rgba(255,255,255,1)'


class RequestStage(models.Model):
    _name = "request.stage"
    _inherit = [
        'generic.mixin.name_with_code',
    ]
    _description = "Request Stage"
    _order = "sequence"

    # Defined in generic.mixin.name_with_code
    name = fields.Char()
    code = fields.Char()

    type_id = fields.Many2one(
        'request.stage.type', string="Stage Type", index=True,
        ondelete="restrict")
    active = fields.Boolean(
        default=True, index=True)

    sequence = fields.Integer(default=5, index=True)
    request_type_id = fields.Many2one(
        'request.type', 'Request Type', ondelete='cascade',
        required=True, index=True)
    description = fields.Text(translate=True)
    help_html = fields.Html("Help", translate=True)
    bg_color = fields.Char(default=DEFAULT_BG_COLOR, string="Backgroung Color")
    label_color = fields.Char(default=DEFAULT_LABEL_COLOR)

    # Custom colors
    use_custom_colors = fields.Boolean(
        help="Select colors from the palette manually")
    res_bg_color = fields.Char(
        compute='_compute_custom_colors', readonly=True,
        string="Backgroung Color")
    res_label_color = fields.Char(
        compute='_compute_custom_colors',
        readonly=True, string="Label Color")

    # Route relations
    route_in_ids = fields.One2many(
        'request.stage.route', 'stage_to_id', 'Incoming routes')
    route_in_count = fields.Integer(
        'Routes In', compute='_compute_routes_in_count', readonly=True)
    route_out_ids = fields.One2many(
        'request.stage.route', 'stage_from_id', 'Outgoing routes')
    route_out_count = fields.Integer(
        'Routes Out', compute='_compute_routes_out_count', readonly=True)

    previous_stage_ids = fields.Many2many(
        'request.stage', 'request_stage_prev_stage_ids_rel',
        'stage_id', 'prev_stage_id',
        string='Previous stages', compute='_compute_previous_stage_ids',
        store=True)
    closed = fields.Boolean(
        index=True, help="Is request on this stage closed?")

    _sql_constraints = [
        ('stage_name_uniq',
         'UNIQUE (request_type_id, name)',
         'Stage name must be uniq for request type'),
        ('stage_code_uniq',
         'UNIQUE (request_type_id, code)',
         'Stage code must be uniq for request type'),
    ]

    @api.depends('request_type_id', 'request_type_id.stage_ids',
                 'request_type_id.route_ids',
                 'request_type_id.route_ids.stage_from_id',
                 'request_type_id.route_ids.stage_to_id')
    def _compute_previous_stage_ids(self):
        for stage in self:
            route_ids = stage.request_type_id.route_ids.filtered(
                lambda r: r.stage_to_id == stage)

            stage_ids = route_ids.mapped('stage_from_id')
            stage.previous_stage_ids = stage_ids

    @api.depends('route_in_ids')
    def _compute_routes_in_count(self):
        for record in self:
            record.route_in_count = len(record.route_in_ids)

    @api.depends('route_out_ids')
    def _compute_routes_out_count(self):
        for record in self:
            record.route_out_count = len(record.route_out_ids)

    @api.depends('bg_color', 'label_color', 'type_id', 'use_custom_colors')
    def _compute_custom_colors(self):
        for rec in self:
            if rec.use_custom_colors:
                rec.res_bg_color = rec.bg_color
                rec.res_label_color = rec.label_color
            elif rec.type_id:
                rec.res_bg_color = rec.type_id.bg_color
                rec.res_label_color = rec.type_id.label_color
            else:
                rec.res_bg_color = DEFAULT_BG_COLOR
                rec.res_label_color = DEFAULT_LABEL_COLOR

    def action_show_incoming_routes(self):
        self.ensure_one()
        action = self.env.ref(
            'generic_request.action_request_stage_incoming_routes')
        result = action.read()[0]
        result['context'] = {
            'default_stage_to_id': self.id,
            'default_request_type_id': self.request_type_id.id,
        }
        return result

    def action_show_outgoing_routes(self):
        self.ensure_one()
        action = self.env.ref(
            'generic_request.action_request_stage_outgoing_routes')
        result = action.read()[0]
        result['context'] = {
            'default_stage_from_id': self.id,
            'default_request_type_id': self.request_type_id.id,
        }
        return result

    def unlink(self):
        messages = []
        for record in self:
            if record.route_out_ids or record.route_in_ids:
                routes = "\n".join(
                    ["- %s" % r.display_name for r in record.route_in_ids] +
                    ["- %s" % r.display_name for r in record.route_out_ids])
                msg = _(
                    "Cannot delete stage %s because it is referenced from "
                    "following routes:\n%s"
                ) % (
                    record.display_name,
                    routes
                )
                messages += [msg]
        if messages:
            raise exceptions.ValidationError("\n\n".join(messages))
        return super(RequestStage, self).unlink()

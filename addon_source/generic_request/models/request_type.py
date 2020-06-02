from odoo import models, fields, api, _
from .request_request import (AVAILABLE_PRIORITIES,
                              AVAILABLE_IMPACTS,
                              AVAILABLE_URGENCIES)


class RequestType(models.Model):
    _name = "request.type"
    _inherit = [
        'mail.thread',
        'generic.mixin.name_with_code',
    ]
    _description = "Request Type"

    name = fields.Char(copy=False)
    code = fields.Char(copy=False)
    kind_id = fields.Many2one('request.kind', index=True)
    active = fields.Boolean(default=True, index=True)
    description = fields.Text(translate=True)
    note_html = fields.Html(
        translate=True,
        help="Short note about request type, that will"
             " be displayed just before request text.")
    instruction_html = fields.Html(translate=True)
    default_request_text = fields.Html(translate=True)
    help_html = fields.Html(translate=True)
    category_ids = fields.Many2many(
        'request.category',
        'request_type_category_rel', 'type_id', 'category_id',
        'Categories', required=False, index=True)

    # Priority configuration
    complex_priority = fields.Boolean(
        default=False,
        help="When creating request, users select "
             "Impact and Urgency of request. Priority "
             "will be automatically computed depending on "
             "these parameters"
    )
    default_priority = fields.Selection(
        selection=AVAILABLE_PRIORITIES,
        default='3'
    )
    default_impact = fields.Selection(
        selection=AVAILABLE_IMPACTS,
        default='2'
    )
    default_urgency = fields.Selection(
        selection=AVAILABLE_URGENCIES,
        default='2'
    )

    # Stages
    stage_ids = fields.One2many(
        'request.stage', 'request_type_id', string='Stages', copy=True)
    stage_count = fields.Integer(
        compute='_compute_stage_count', readonly=True)
    start_stage_id = fields.Many2one(
        'request.stage', ondelete='set null',
        compute='_compute_start_stage_id', readonly=True, store=True,
        help="The initial stage for new requests of this type. To change, "
             "on the Stages page, click the crossed arrows icon and drag "
             "the desired stage to the top of the list.")
    color = fields.Char(default='rgba(240,240,240,1)')

    # Routes
    route_ids = fields.One2many(
        'request.stage.route', 'request_type_id',
        string='Stage Routes')
    route_count = fields.Integer(
        'Routes', compute='_compute_route_count', readonly=True)

    sequence_id = fields.Many2one(
        'ir.sequence', 'Sequence', ondelete='restrict',
        help="Use this sequence to generate names for requests for this type")

    # Requests
    request_ids = fields.One2many(
        'request.request', 'type_id', 'Requests', readonly=True, copy=False)
    request_count = fields.Integer(
        'All Requests', compute='_compute_request_count', readonly=True)
    request_open_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Open Requests")
    request_closed_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Closed Requests")

    # Notification Settins
    send_default_created_notification = fields.Boolean(default=True)
    created_notification_show_request_text = fields.Boolean(default=True)
    created_notification_show_response_text = fields.Boolean(default=False)
    send_default_assigned_notification = fields.Boolean(default=True)
    assigned_notification_show_request_text = fields.Boolean(default=True)
    assigned_notification_show_response_text = fields.Boolean(default=False)
    send_default_closed_notification = fields.Boolean(default=True)
    closed_notification_show_request_text = fields.Boolean(default=True)
    closed_notification_show_response_text = fields.Boolean(default=True)
    send_default_reopened_notification = fields.Boolean(default=True)
    reopened_notification_show_request_text = fields.Boolean(default=True)
    reopened_notification_show_response_text = fields.Boolean(default=False)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Name must be unique.'),
        ('code_uniq',
         'UNIQUE (code)',
         'Code must be unique.'),
    ]

    @api.depends('request_ids')
    def _compute_request_count(self):
        RequestRequest = self.env['request.request']
        for record in self:
            record.request_count = len(record.request_ids)
            record.request_closed_count = RequestRequest.search_count([
                ('closed', '=', True),
                ('type_id', '=', record.id)
            ])
            record.request_open_count = RequestRequest.search_count([
                ('closed', '=', False),
                ('type_id', '=', record.id)
            ])

    @api.depends('stage_ids')
    def _compute_stage_count(self):
        for record in self:
            record.stage_count = len(record.stage_ids)

    @api.depends('route_ids')
    def _compute_route_count(self):
        for record in self:
            record.route_count = len(record.route_ids)

    @api.depends('stage_ids', 'stage_ids.sequence',
                 'stage_ids.request_type_id')
    def _compute_start_stage_id(self):
        """ Compute start stage for requests of this type
            using following logic:

            - stages have field 'sequence'
            - stages are ordered by value of this field.
            - it is possible from ui to change stage order by dragging them
            - get first stage for stages related to this type

        """
        for rtype in self:
            if rtype.stage_ids:
                rtype.start_stage_id = rtype.stage_ids.sorted(
                    key=lambda r: r.sequence)[0]
            else:
                rtype.start_stage_id = False

    def _create_default_stages_and_routes(self):
        self.ensure_one()
        stage_new = self.env['request.stage'].create({
            'name': _('New'),
            'code': 'new',
            'request_type_id': self.id,
            'sequence': 5,
            'type_id': self.env.ref(
                'generic_request.request_stage_type_draft').id,
        })
        stage_close = self.env['request.stage'].create({
            'name': _('Closed'),
            'code': 'close',
            'request_type_id': self.id,
            'sequence': 10,
            'closed': True,
            'type_id': self.env.ref(
                'generic_request.request_stage_type_closed_ok').id,
        })
        self.env['request.stage.route'].create({
            'name': _('Close'),
            'stage_from_id': stage_new.id,
            'stage_to_id': stage_close.id,
            'request_type_id': self.id,
        })

    def name_get(self):
        # This is required to avoid access rights errors when tracking values
        # in chatter. (At least in Odoo 10.0)
        return super(RequestType, self.sudo()).name_get()

    @api.model
    def create(self, vals):
        r_type = super(RequestType, self).create(vals)

        if not r_type.start_stage_id and self.env.context.get(
                'create_default_stages'):
            r_type._create_default_stages_and_routes()

        return r_type

    def action_request_type_diagram(self):
        self.ensure_one()
        action = self.env.ref(
            'generic_request'
            '.action_type_window').read()[0]
        action.update({
            'res_model': 'request.type',
            'res_id': self.id,
            'views': [(False, 'diagram_plus'), (False, 'form')],
            'context': {
                'default_request_type_id': self.id,
            },
        })
        return action

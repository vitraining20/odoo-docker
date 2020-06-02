from odoo import models, fields, api


class RequestCategory(models.Model):
    _name = "request.category"
    _inherit = [
        'generic.mixin.parent.names',
        'mail.thread',
        'generic.mixin.name_with_code',
    ]
    _description = "Request Category"
    _order = 'sequence, name'

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'

    # Defined in generic.mixin.name_with_code
    name = fields.Char()
    code = fields.Char()

    parent_id = fields.Many2one(
        'request.category', 'Parent', index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)

    active = fields.Boolean(default=True, index=True)

    description = fields.Text(translate=True)
    help_html = fields.Html(translate=True)

    # Stat
    request_ids = fields.One2many(
        'request.request', 'category_id', 'Requests', readonly=True)
    request_count = fields.Integer(
        'All Requests', compute='_compute_request_count', readonly=True)
    request_open_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Open Requests")
    request_closed_count = fields.Integer(
        compute="_compute_request_count", readonly=True,
        string="Closed Requests")

    request_type_ids = fields.Many2many(
        'request.type',
        'request_type_category_rel', 'category_id', 'type_id',
        string="Request types")
    request_type_count = fields.Integer(
        compute='_compute_request_type_count')
    sequence = fields.Integer(index=True, default=5)
    color = fields.Integer()  # for many2many_tags widget

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (parent_id, name)',
         'Category name must be unique.'),
    ]

    @api.depends('request_ids')
    def _compute_request_count(self):
        RequestRequest = self.env['request.request']
        for record in self:
            record.request_count = len(record.request_ids)
            record.request_closed_count = RequestRequest.search_count([
                ('closed', '=', True),
                ('category_id', '=', record.id)
            ])
            record.request_open_count = RequestRequest.search_count([
                ('closed', '=', False),
                ('category_id', '=', record.id)
            ])

    @api.depends('request_type_ids')
    def _compute_request_type_count(self):
        for record in self:
            record.request_type_count = len(record.request_type_ids)

    def name_get(self):
        # This is required to avoid access rights errors when tracking values
        # in chatter. (At least in Odoo 10.0)
        return super(RequestCategory, self.sudo()).name_get()

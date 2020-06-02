from odoo import models, fields, api


class RequestKind(models.Model):
    _name = 'request.kind'
    _inherit = [
        'mail.thread',
        'generic.mixin.name_with_code',
        'generic.mixin.uniq_name_code',
    ]
    _description = 'Request kind'
    _order = 'sequence ASC'

    # Defined in generic.mixin.name_with_code
    name = fields.Char(string='Kind')
    code = fields.Char()

    description = fields.Text(translate=True)
    active = fields.Boolean(index=True, default=True)
    request_type_ids = fields.One2many(
        'request.type', 'kind_id', string='Request Types')
    request_type_count = fields.Integer(
        compute='_compute_request_type_count', readonly=True)
    request_ids = fields.One2many(
        'request.request', 'kind_id', string='Requests')
    request_count = fields.Integer(
        compute='_compute_request_count', readonly=True)

    sequence = fields.Integer(index=True, default=5)

    request_open_count = fields.Integer(
        compute="_compute_request_count", readonly=True)
    request_closed_count = fields.Integer(
        compute="_compute_request_count", readonly=True)

    menuitem_id = fields.Many2one(
        'ir.ui.menu')
    menuaction_id = fields.Many2one(
        'ir.actions.act_window')
    menuitem_name = fields.Char(
        related='menuitem_id.name', readonly=False)
    menuaction_name = fields.Char(
        related='menuaction_id.name', readonly=False)
    menuitem_toggle = fields.Boolean(
        compute='_compute_menuitem_toggle',
        inverse='_inverse_menuitem_toggle',
        string='Show Menuitem',
        help="Show/Hide menuitem for requests of this kind. "
             "To see new menuitem, please reload the page."
    )

    @api.depends('request_type_ids')
    def _compute_request_type_count(self):
        for record in self:
            record.request_type_count = len(record.request_type_ids)

    @api.depends('request_ids')
    def _compute_request_count(self):
        RequestRequest = self.env['request.request']
        for record in self:
            record.request_count = len(record.request_ids)
            record.request_closed_count = RequestRequest.search_count([
                ('closed', '=', True),
                ('kind_id', '=', record.id)
            ])
            record.request_open_count = RequestRequest.search_count([
                ('closed', '=', False),
                ('kind_id', '=', record.id)
            ])

    @api.depends('menuitem_id')
    def _compute_menuitem_toggle(self):
        for rec in self:
            rec.menuitem_toggle = bool(rec.menuitem_id)

    def _inverse_menuitem_toggle(self):
        for rec in self:
            if rec.menuitem_toggle:
                rec.menuaction_id = rec._create_menuaction()
                rec.menuitem_id = rec._create_menuitem()
            else:
                rec.menuitem_id.unlink()
                rec.menuaction_id.unlink()

    def _create_menuaction(self):
        self.ensure_one()
        return self.env.ref(
            'generic_request.action_request_window'
        ).copy({
            'name': self.name,
            'domain': [('kind_id', '=', self.id)],
        })

    def _create_menuitem(self):
        self.ensure_one()
        parent_menu = self.env.ref('generic_request.menu_request')
        return self.env['ir.ui.menu'].create({
            'name': self.name,
            'parent_id': parent_menu.id,
            'action': ('ir.actions.act_window,%d' %
                       self.menuaction_id.id),
            'sequence': 100 + self.sequence,
        })

    def action_show_request_type(self):
        self.ensure_one()
        action = self.env.ref(
            'generic_request.action_type_window'
        ).read()[0]
        ctx = dict(self.env.context)
        ctx.update({
            'default_kind_id': self.id})
        return dict(
            action,
            context=ctx,
            domain=[('kind_id', '=', self.id)])

    def action_show_all_requests(self):
        self.ensure_one()
        action = self.env.ref(
            'generic_request.action_request_window'
        ).read()[0]
        ctx = dict(self.env.context)
        ctx.update({
            'search_default_kind_id': self.id})
        return dict(
            action,
            context=ctx,
            domain=[('kind_id', '=', self.id)])

    def action_show_open_requests(self):
        self.ensure_one()
        action = self.env.ref(
            'generic_request.action_request_window'
        ).read()[0]
        ctx = dict(self.env.context)
        ctx.update({
            'search_default_filter_open': 1,
            'search_default_kind_id': self.id})
        return dict(
            action,
            context=ctx,
            domain=[('kind_id', '=', self.id)])

    def action_show_closed_requests(self):
        self.ensure_one()
        action = self.env.ref(
            'generic_request.action_request_window'
        ).read()[0]
        ctx = dict(self.env.context)
        ctx.update({
            'search_default_filter_closed': 1,
            'search_default_kind_id': self.id})
        return dict(
            action,
            context=ctx,
            domain=[('kind_id', '=', self.id)])

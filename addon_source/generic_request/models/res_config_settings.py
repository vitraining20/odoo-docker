from odoo import fields, models, api

FEATURE_MODULES = [
    'generic_assignment_hr',
    'generic_assignment_team',
    'generic_request_assignment',
    'generic_request_action',
    'generic_request_action_condition',
    'generic_request_action_project',
    'generic_request_action_subrequest',
    'generic_request_sla',
    'generic_request_sla_log',
    'generic_request_field',
    'generic_request_parent',
    'generic_request_related_doc',
    'generic_request_related_requests',
    'generic_request_reopen_as',
    'generic_request_route_auto',
    'generic_request_service',
    'generic_request_tag',
    'generic_request_mail',
    'generic_request_api',
    'generic_request_survey',
    'generic_request_action_survey',
    'generic_request_action_tag',
]


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Modules available
    module_generic_assignment_hr = fields.Boolean(
        string="HR Assignments")
    module_generic_assignment_team = fields.Boolean(
        string="Team Assignments")
    module_generic_request_assignment = fields.Boolean(
        string="Use Custom Assignment Policies")
    module_generic_request_action = fields.Boolean(
        string="Use Automated Actions")
    module_generic_request_action_condition = fields.Boolean(
        string="Conditional Actions")
    module_generic_request_action_project = fields.Boolean(
        string="Tasks")
    module_generic_request_action_subrequest = fields.Boolean(
        string="Subrequests")
    module_generic_request_sla = fields.Boolean(
        string="Use Service Level Agreements")
    module_generic_request_sla_log = fields.Boolean(
        string="Log Service Level")
    module_generic_request_field = fields.Boolean(
        string="Use Custom Fields in Requests")
    module_generic_request_parent = fields.Boolean(
        string="Use Subrequests")
    module_generic_request_related_doc = fields.Boolean(
        string="Documents Related to Requests")
    module_generic_request_related_requests = fields.Boolean(
        string="Related Requests")
    module_generic_request_reopen_as = fields.Boolean(
        string="Reopen Requests")
    module_generic_request_route_auto = fields.Boolean(
        string="Use Automatic Routes")
    module_generic_request_service = fields.Boolean(
        string="Use Services")
    module_generic_request_tag = fields.Boolean(
        string="Use Tags")
    module_generic_request_mail = fields.Boolean(
        string="Use Mail Sources")
    module_generic_request_api = fields.Boolean(
        string="Use API endpoints")
    module_generic_request_survey = fields.Boolean(
        string="Surveys")
    module_generic_request_action_survey = fields.Boolean(
        string="Surveys")
    module_generic_request_action_tag = fields.Boolean(
        string="Tags")

    # Modules available (helpers)
    need_install_generic_assignment_hr = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_assignment_team = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_assignment = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_condition = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_project = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_subrequest = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_sla = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_sla_log = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_field = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_parent = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_related_doc = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_related_requests = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_reopen_as = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_route_auto = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_service = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_tag = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_mail = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_api = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_survey = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_survey = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)
    need_install_generic_request_action_tag = fields.Boolean(
        compute="_compute_generic_request_modules_can_install", readonly=True)

    request_event_live_time = fields.Integer(
        related='company_id.request_event_live_time', readonly=False)
    request_event_live_time_uom = fields.Selection(
        related='company_id.request_event_live_time_uom',
        readonly=False,
        help='Units of Measure'
    )
    request_event_auto_remove = fields.Boolean(
        related='company_id.request_event_auto_remove', readonly=False)

    @api.depends('company_id')
    def _compute_generic_request_modules_can_install(self):
        available_module_names = self.env['ir.module.module'].search([
            ('name', 'in', FEATURE_MODULES),
            ('state', '!=', 'uninstallable'),
        ]).mapped('name')
        for record in self:
            for module in FEATURE_MODULES:
                record['need_install_%s' % module] = (
                    module not in available_module_names
                )

from odoo import models, fields


class GenericEventCategory(models.Model):
    _name = 'request.event.category'
    _inherit = ['generic.mixin.name_with_code',
                'generic.mixin.uniq_name_code']
    _order = 'name, id'
    _description = 'Request Event Category'

    name = fields.Char(index=True, translate=True, required=True)
    code = fields.Char(index=True, required=True)
    description = fields.Text(translate=True)

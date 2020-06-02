from odoo import models, fields, api, tools


class RequestEventType(models.Model):
    _name = "request.event.type"
    _inherit = ['generic.mixin.name_with_code',
                'generic.mixin.uniq_name_code']
    _description = "Request Event Type"
    _log_access = False

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    category_id = fields.Many2one(
        'request.event.category',
        ondelete='restrict', index=True, required=True)

    @api.model
    @tools.ormcache('code')
    def get_event_type_id(self, code):
        record = self.search(
            [('code', '=', code)], limit=1)
        if record:
            return record.id
        return False

    def get_event_type(self, code):
        event_type_id = self.get_event_type_id(code)
        if event_type_id:
            return self.browse(event_type_id)
        return self.browse()

    def name_get(self):
        return [(rec.id, '%s / %s' % (
            rec.category_id.name, rec.name)) for rec in self]

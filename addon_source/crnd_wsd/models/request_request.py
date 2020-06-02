from odoo import models, fields


class RequestRequest(models.Model):
    _name = 'request.request'
    _inherit = [
        'request.request',
        'portal.mixin',
    ]
    _mail_post_access = 'read'

    # Set this to compute with sudo to avoid access rights conflicts
    activity_date_deadline = fields.Date(compute_sudo=True)
    created_by_avatar = fields.Binary(
        "Creator (Avatar)", related='created_by_id.image_128')
    author_avatar = fields.Binary(
        "Author (Avatar)", related='author_id.image_128')
    assignee_avatar = fields.Binary(
        "Assignee (Avatar)", related='user_id.image_128')
    closed_by_avatar = fields.Binary(
        "Closed By (Avatar)", related='closed_by_id.image_128')

    def _compute_access_url(self):
        res = super(RequestRequest, self)._compute_access_url()
        for request in self:
            request.access_url = '/requests/request/%s' % request.id
        return res

    def get_access_action(self, access_uid=None):
        """ Redirect portal users to website interface. """
        self.ensure_one()

        user, record = self.env.user, self
        if access_uid:
            user = self.env['res.users'].sudo().browse(access_uid)
            record = self.with_user(user)
        if user.share:
            return {
                'type': 'ir.actions.act_url',
                'url': record.access_url,
                'target': 'self',
                'res_id': self.id,
            }
        return super(RequestRequest, self).get_access_action(access_uid)

    def _notification_recipients(self, message, groups):
        """ Display access button in mails to portal users
        """
        self.ensure_one()
        groups = super(RequestRequest, self)._notification_recipients(
            message, groups)

        # pylint: disable=unused-variable
        for group_name, group_method, group_data in groups:
            if group_name == 'customer':
                continue
            group_data['has_button_access'] = True

        return groups

    def action_show_on_website(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.access_url,
            'target': 'self',
        }

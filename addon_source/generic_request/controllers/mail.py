import logging
from odoo import http
from odoo.addons.mail.controllers.main import MailController

_logger = logging.getLogger(__name__)


class RequestMailController(MailController):

    # Handle mail view links. We do not use standard Odoo url, because we
    # show requests to authorized users only
    @http.route("/mail/view/request/<int:request_id>",
                type='http', auth='user', website=True)
    def mail_action_view_request(self, request_id, **kwargs):
        return super(
            RequestMailController, self
        ).mail_action_view(
            model='request.request', res_id=request_id, **kwargs)

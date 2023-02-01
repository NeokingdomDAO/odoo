from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import AccessDenied

class Users(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_login_domain(self, login):
        return expression.OR([
            super()._get_login_domain(login),
            [('ethereum_address', '=', login)]
        ])

    def _check_credentials(self, password, env):
        try:
            return super()._check_credentials(password, env)
        except AccessDenied:
            passwd_allowed = env['interactive'] or not self.env.user._rpc_api_keys_only()
            if passwd_allowed and self.env.user.active and env['auth.jwt.w3.validator'].is_signing_token_valid(password):
                return
            raise AccessDenied

    def _get_session_token_fields(self):
        return super()._get_session_token_fields() | {'ethereum_address'}

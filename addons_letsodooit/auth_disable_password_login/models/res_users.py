from odoo import api, fields, models, _
from odoo.exceptions import AccessDenied, UserError

class Users(models.Model):
    _inherit = 'res.users'

    disable_password_login = fields.Boolean(
        string='Disable Password Login',
        default=False
    )

    def _unset_password(self):
        self.ensure_one()
        self.env.cr.execute(
            'UPDATE res_users SET password=null WHERE id=%s',
            (self.id,)
        )
        self.invalidate_cache(['password'], [self.id])

    @api.model_create_multi
    def create(self, values_list):
        users = super().create(values_list)
        for user in users:
            if user.disable_password_login:
                user._unset_password()
        return users

    def write(self, values):
        result = super().write(values)
        for user in self:
            if user.disable_password_login:
                user._unset_password()
        return result

    def action_reset_password(self):
        if self.filtered(lambda user: user.disable_password_login):
            raise UserError(_("You cannot perform this action on an user with password login being disbaled."))
        return super().action_reset_password()

    def _check_credentials(self, password, user_agent_env):
        if self.env.user.disable_password_login:
            raise AccessDenied(_("For this user password login is disabled."))
        return super()._check_credentials(password, user_agent_env)

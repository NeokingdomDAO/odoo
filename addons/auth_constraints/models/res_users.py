from odoo import fields, models

class User(models.Model):
    _inherit = 'res.users'

    def write(self, values):
        if values.get('ethereum_address', False):
            values['disable_password_login'] = True
        return super().write(values)

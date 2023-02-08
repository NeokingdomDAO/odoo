from odoo import fields, models

class User(models.Model):
    _inherit = 'res.users'

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + [
            'ethereum_address',
        ]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + [
            'ethereum_address',
        ]

    ethereum_address = fields.Char('Ethereum Address')

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            values['ethereum_address'] = values.get('ethereum_address', '').lower()
        return super().create(vals_list)

    def write(self, values):
        if 'ethereum_address' in values:
            values['ethereum_address'] = values['ethereum_address'].lower()
        return super().write(values)

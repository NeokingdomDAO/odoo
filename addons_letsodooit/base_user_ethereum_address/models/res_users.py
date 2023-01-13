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

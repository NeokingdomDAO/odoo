from odoo import fields, models

class User(models.Model):
    _inherit = 'res.users'

    ethereum_address = fields.Char('Ethereum Address')

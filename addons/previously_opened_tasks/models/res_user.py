from odoo import fields, models


class NeokPotResUser(models.Model):
    _inherit = 'res.users'

    show_pot = fields.Boolean(string='Show previously opened tasks', default=True, help='Only the last 10 tasks will be shown.')

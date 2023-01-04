from odoo import fields, models, _

class Task(models.Model):
    _inherit = 'project.task'

    tier_id = fields.Many2one('account.analytic.tier', string='Tier', required=True) 

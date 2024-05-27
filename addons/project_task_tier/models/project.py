from odoo import api, fields, models, _


class Task(models.Model):
    _inherit = 'project.task'

    # ! tier_id on task is now deprecated and only used to store old data !
    # all related logic is removed
    tier_id = fields.Many2one(
        comodel_name='account.analytic.tier',
        string='Tier',
        required=False
    )

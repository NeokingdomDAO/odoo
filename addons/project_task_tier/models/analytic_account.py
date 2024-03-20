from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    task_stage_id = fields.Many2one('project.task.type', related='task_id.stage_id', string='Task Stage')
    tier_id = fields.Many2one('account.analytic.tier', related='task_id.tier_id', string='Task Tier')
    token_amount = fields.Float('Tokens', compute='_compute_token_amount', store=True)

    @api.depends('tier_id', 'unit_amount')
    def _compute_token_amount(self):
        for line in self:
            line.token_amount = line.tier_id.calculate_token_amount(line.unit_amount)

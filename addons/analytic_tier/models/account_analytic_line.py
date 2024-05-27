from odoo import fields, models, api
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _default_tier_id(self):
        if self.employee_id.exists() and not self.employee_id.tier_id.exists():
            raise ValidationError(
                'Contributor\'s tier is not defined. Please set the applicable tier for the contributor first.')

        return self.employee_id.tier_id

    tier_id = fields.Many2one(
        comodel_name='account.analytic.tier',
        default=_default_tier_id,
        string='Tier'
    )
    tokenized = fields.Boolean()
    token_amount = fields.Float('Tokens', compute='_compute_token_amount', store=True)

    @api.depends('tier_id', 'unit_amount')
    def _compute_token_amount(self):
        for line in self:
            line.token_amount = line.tier_id.calculate_token_amount(line.unit_amount)

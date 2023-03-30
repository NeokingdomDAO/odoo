from odoo import fields, models

class AccountAnalyticTier(models.Model):
    _name = 'account.analytic.tier'
    _description = 'Account Analytic Tier'

    name = fields.Char(
        required=True
    )
    token_per_hour = fields.Float(
        string='Token Per Hour',
        default=0.0
    )

    def calculate_token_amount(self, hours):
        return self.token_per_hour * hours


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    tier_id = fields.Many2one(
        comodel_name='account.analytic.tier',
        string='Tier'
    )
    tokenized = fields.Boolean()

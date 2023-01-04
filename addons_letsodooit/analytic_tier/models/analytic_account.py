from odoo import fields, models

class AccountAnalyticTier(models.Model):
    _name = 'account.analytic.tier'
    _description = 'Account Analytic Tier'

    name = fields.Char('Name')
    token_per_hour = fields.Float('Token per hour')

    def calculate_token_amount(self, hours):
        return self.token_per_hour * hours


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    tier_id = fields.Many2one('account.analytic.tier', string='Tier')
    tokenized = fields.Boolean('Tokenized')

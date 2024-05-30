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

    def _update_tier_based_on_employee(self, vals):
        if ('employee_id' in vals) and (('tier_id' not in vals) or not vals.get('tier_id', False)):
            employee = self.env['hr.employee'].browse(vals['employee_id'])

            if not employee.tier_id.exists():
                raise ValidationError(
                    'Contributor\'s tier is not defined. Please set the applicable tier for the contributor first.')

            vals['tier_id'] = employee.tier_id.id

        return vals

    def write(self, vals):
        vals = self._update_tier_based_on_employee(vals)
        res = super(AccountAnalyticLine, self).write(vals)

        for _time_entry in self:
            if not _time_entry.tier_id.exists():
                raise ValidationError('Please ensure that the time entry has a valid tier assigned to it.')

        return res

    @api.model_create_multi
    def create(self, vals):
        for i, val in enumerate(vals):
            if isinstance(val, dict):
                vals[i] = self._update_tier_based_on_employee(val)

        return super(AccountAnalyticLine, self).create(vals)

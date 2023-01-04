from odoo import api, fields, models

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        self.tier_id = self.employee_id.tier_id if self.employee_id.tier_id else self.tier_id

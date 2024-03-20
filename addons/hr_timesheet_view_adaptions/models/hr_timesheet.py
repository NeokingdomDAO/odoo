from odoo import api, fields, models, _

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    approval_date = fields.Date(related='task_id.approval_date')

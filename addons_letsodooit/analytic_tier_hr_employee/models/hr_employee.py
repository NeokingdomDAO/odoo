from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    tier_id = fields.Many2one(
        comodel_name='account.analytic.tier',
        string='Default Tier'
    )

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    tier_id = fields.Many2one(
        comodel_name='account.analytic.tier',
        related='employee_id.tier_id',
        compute_sudo=True
    )

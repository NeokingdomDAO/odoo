from odoo import api, fields, models, _

class Task(models.Model):
    _inherit = 'project.task'

    tier_id = fields.Many2one('account.analytic.tier', string='Tier', required=True) 

    @api.onchange('user_id')
    def onchange_user_id(self):
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)], limit=1)
        self.tier_id = employee_id.tier_id

from odoo import models, api, fields, _
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.constrains('user_id')
    def check_no_time_tracked(self):
        for task in self:
            if self.env['account.analytic.line'].search_count([('task_id', '=', task.id)]):
                raise UserError(_("You cannot reassign a task after time has been tracked!"))

    @api.constrains('stage_id')
    def check_pre_final_stage(self):
        for line in self.env['account.analytic.line'].search([('task_id', 'in', self.ids)]):
            if line.task_id.stage_id.is_pre_final() and line.name == '/':
                raise UserError(_('Please set a proper description to every timesheet entry before setting this task to done!'))

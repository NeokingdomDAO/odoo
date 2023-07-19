from odoo import models, api, fields, _
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.constrains('user_ids')
    def ensure_employee_part_of_assignees(self):
        for task in self:
            timesheet_ids = self.env['account.analytic.line'].search([('task_id', '=', task.id)])
            for employee_id in timesheet_ids.employee_id:
                if not employee_id.user_id or (task.user_ids and employee_id.user_id not in task.user_ids):
                    raise UserError(_("There is a mismatch between the person who tracked time and the assignees for this task. Please fix it first!"))

    @api.constrains('stage_id')
    def check_pre_final_stage(self):
        for line in self.env['account.analytic.line'].search([('task_id', 'in', self.ids)]):
            if line.task_id.stage_id.is_pre_final() and line.name == '/':
                raise UserError(_('Please set a proper description to every timesheet entry before setting this task to done!'))

    def _update_analytic_lines(self):
        archived_tasks = self.filtered(lambda task: not task.active)
        analytic_line_ids = self.env['account.analytic.line'].search([('task_id', 'in', archived_tasks.ids)])
        analytic_line_ids.unlink()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._update_analytic_lines()
        return records

    def write(self, values):
        result = super().write(values)
        self._update_analytic_lines()
        return result

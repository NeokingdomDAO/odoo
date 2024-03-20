from odoo import models, api, fields, _

class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _update_analytic_line_active(self):
        archived_tasks = self.filtered(lambda task: not task.active)
        analytic_line_ids = self.env['account.analytic.line'].search([('task_id', 'in', archived_tasks.ids)])
        analytic_line_ids.unlink()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._update_analytic_line_active()
        return records

    def write(self, values):
        result = super().write(values)
        self._update_analytic_line_active()
        return result

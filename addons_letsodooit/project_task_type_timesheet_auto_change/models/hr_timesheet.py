from odoo import api, fields, models, _

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for task_id in records.mapped('task_id'):
            if task_id.stage_id.is_initial():
                task_id.write({
                    'stage_id': self.env['project.task.type'].get_post_initial_stage_for_task(task_id).id
                })
        return records

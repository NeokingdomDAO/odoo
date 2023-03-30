from odoo import api, models, _
from odoo.exceptions import UserError

class Task(models.Model):
    _inherit = 'project.task'

    @api.constrains('parent_id', 'date_deadline')
    def check_date_deadline_lower_than_parent(self):
        for task in self:
            if task.parent_id and task.date_deadline > task.parent_id.date_deadline:
                raise UserError(_('Please ensure that the deadline of the task is not greater than the deadline of the parent task!'))

    def write(self, values):
        for task in self:
            if task.stage_id.is_final() and not self.env.context.get('force_final_stage', False):
                raise UserError(_('You cannot change a task which is in a final stage!'))
        return super().write(values)

    def unlink(self):
        for task in self:
            if task.stage_id.is_final() and not self.env.context.get('force_final_stage', False):
                raise UserError(_('You cannot delete a task which is in a final stage!'))
        return super().unlink()

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    @api.constrains('sequence')
    def ensure_special_stages_ordered(self):
        for stage in self:
            if stage.stage_type in ['initial', 'post_initial', 'pre_final', 'final']:
                for project in stage.project_ids:
                    initial_stage = stage.get_initial_stage_for_project(project)
                    post_initial_stage = stage.get_post_initial_stage_for_project(project)
                    pre_final_stage = stage.get_pre_final_stage_for_project(project)
                    final_stage = stage.get_final_stage_for_project(project)
                    if initial_stage and post_initial_stage and not initial_stage.sequence < post_initial_stage.sequence:
                        raise UserError(_('Please ensure that the sequence of the initial stage is lower than the sequence of the post initial stage!'))
                    if post_initial_stage and pre_final_stage and not post_initial_stage.sequence < pre_final_stage.sequence:
                        raise UserError(_('Please ensure that the sequence of the post initial stage is lower than the sequence of the pre final stage!'))
                    if pre_final_stage and final_stage and not pre_final_stage.sequence < final_stage.sequence:
                        raise UserError(_('Please ensure that the sequence of the pre final stage is lower than the sequence of the final stage!'))

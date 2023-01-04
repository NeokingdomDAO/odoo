from odoo import api, models, _
from odoo.exceptions import UserError

class Task(models.Model):
    _inherit = 'project.task'

    @api.constrains('stage_id')
    def check_is_final_stage(self):
        for task in self:
            if task.stage_id.is_final():
                raise UserError(_('You cannot change/delete a task which is in a final stage!'))

    @api.constrains('parent_id', 'date_deadline')
    def check_date_deadline_lower_than_parent(self):
        for task in self:
            if task.parent_id and task.date_deadline > task.parent_id.date_deadline:
                raise UserError(_('Please ensure that the deadline of the task is not greate than the deadline of the parent task!'))

    @api.constrains('stage_id.sequence')
    def ensure_special_stages_ordered(self):
        for task in self:
            if task.stage_id.stage_type in ['initial', 'post_initial', 'pre_final', 'final']:
                initial_stage = task.stage_id.get_initial_stage_for_task(task)
                post_initial_stage = task.stage_id.get_post_initial_stage_for_task(task)
                pre_final_stage = task.stage_id.get_pre_final_stage_for_task(task)
                final_stage = task.stage_id.get_final_stage_for_task(task)
                if not initial_stage.sequence < post_initial_stage.sequence:
                    raise UserError(_('Please ensure that the sequence of the initial stage is lower than the sequence of the post initial stage!'))
                if not post_initial_stage.sequence < pre_final_stage.sequence:
                    raise UserError(_('Please ensure that the sequence of the post initial stage is lower than the sequence of the pre final stage!'))
                if not pre_final_stage.sequence < final_stage.sequence:
                    raise UserError(_('Please ensure that the sequence of the pre final stage is lower than the sequence of the final stage!'))

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

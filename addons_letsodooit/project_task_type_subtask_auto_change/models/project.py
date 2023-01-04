from odoo import api, fields, models

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    subtask_criterion = fields.Selection([('any', 'any'), ('all', 'all')], string='Subtask Criterion', required=True, default='any')

    def is_before(self, stage):
        self.ensure_one()
        stage.ensure_one()
        return self.sequence < stage.sequence

    def is_equal_or_before(self, stage):
        self.ensure_one()
        stage.ensure_one()
        return self == stage or self.is_before(stage)

    def is_after(self, stage):
        self.ensure_one()
        stage.ensure_one()
        return self.sequence > stage.sequence

    def is_equal_or_after(self, stage):
        self.ensure_one()
        stage.ensure_one()
        return self == stage or self.is_after(stage)

class Project(models.Model):
    _inherit = 'project.project'

    def get_stage_by(self, order, limit, search_criterion=None):
        self.ensure_one()
        if not search_criterion:
            search_criterion = []
        search_criterion.append(('project_ids', '=', self.id))
        return self.env['project.task.type'].search(search_criterion, order=order, limit=limit)

    def get_next_all_stage_from(self, stage):
        self.ensure_one()
        stage.ensure_one()
        search_criterion = [('sequence', '>', stage.sequence), ('subtask_criterion', '=', 'all')]
        return self.get_stage_by('sequence asc', 1, search_criterion=search_criterion)

    def get_previous_stage_from(self, stage):
        self.ensure_one()
        stage.ensure_one()
        search_criterion = [('sequence', '<', stage.sequence)]
        return self.get_stage_by('sequence desc', 1, search_criterion=search_criterion)


class Task(models.Model):
    _inherit = 'project.task'

    """
    We compute the stage of a task based on its subtask stages.
    Basically, we check if there is a next 'all' stage (see project_task_type.py) looking from the current task's stage and if just one subtask already reached that stage.
    If so we take the stage right before the 'all' stage as this is the greatest 'any' stage the task should be in.
    If not we take the greatest 'any' stage we can find.

    If there is a subtask with a greater 'any' stage than the next 'all' stage the task should still remain within the stage before the next 'all' stage.
    """
    def compute_stage(self):
        self.ensure_one()
        assert len(self.child_ids) > 0
        smallest_subtask_stage = self.get_smallest_subtask_stage()
        next_all_stage = self.project_id.get_next_all_stage_from(smallest_subtask_stage)
        if next_all_stage and any(subtask.stage_id.is_equal_or_after(next_all_stage) for subtask in self.child_ids):
            stage = self.project_id.get_previous_stage_from(next_all_stage)
        else:
            stage = self.get_greatest_subtask_stage()
        return stage

    def get_subtask_stage_by(self, comparator):
        stage = False
        for subtask in self.child_ids:
            if not stage or comparator(subtask.stage_id, stage):
                stage = subtask.stage_id
        return stage

    def get_smallest_subtask_stage(self):
        self.ensure_one()
        def smaller_than(stage_1, stage_2):
            return stage_1.sequence < stage_2.sequence
        return self.get_subtask_stage_by(smaller_than)

    def get_greatest_subtask_stage(self):
        self.ensure_one()
        def greater_than(stage_1, stage_2):
            return stage_1.sequence > stage_2.sequence
        return self.get_subtask_stage_by(greater_than)

    def update_stage(self):
        self.write({'stage_id': self.compute_stage().id})

    def write(self, values):
        result = super().write(values)
        for parent in self.mapped('parent_id'):
            parent.update_stage()
        return result

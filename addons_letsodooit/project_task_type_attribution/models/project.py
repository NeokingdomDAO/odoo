from odoo import api, fields, models

class ProjectTask(models.Model):
    _inherit = 'project.task'

    stage_id = fields.Many2one('project.task.type', required=True)


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    stage_type = fields.Selection([
        ('initial', 'Initial'),
        ('post_initial', 'Post-Initial'),
        ('pre_final', 'Pre-Final'),
        ('final', 'Final')
    ], string="Stage Type", default=None)

    def is_type(self, given_type):
        self.ensure_one()
        return self.stage_type == given_type

    def is_initial(self):
        return self.is_type('initial')

    def is_post_initial(self):
        return self.is_type('post_initial')

    def is_pre_final(self):
        return self.is_type('pre_final')

    def is_final(self):
        return self.is_type('final')

    @api.model
    def get_stage_for_project_by_stage_type(self, project, stage_type):
        return self.search([
            ('stage_type', '=', stage_type),
            ('project_ids', '=', project.id)
        ], limit=1)

    @api.model
    def get_initial_stage_for_project(self, project):
        return self.get_stage_for_project_by_stage_type(project, 'initial')

    @api.model
    def get_post_initial_stage_for_project(self, project):
        return self.get_stage_for_project_by_stage_type(project, 'post_initial')

    @api.model
    def get_pre_final_stage_for_project(self, project):
        return self.get_stage_for_project_by_stage_type(project, 'pre_final')

    @api.model
    def get_final_stage_for_project(self, project):
        return self.get_stage_for_project_by_stage_type(project, 'final')

    @api.model
    def get_initial_stage_for_task(self, task):
        return self.get_initial_stage_for_project(task.project_id)

    @api.model
    def get_post_initial_stage_for_task(self, task):
        return self.get_post_initial_stage_for_project(task.project_id)

    @api.model
    def get_pre_final_stage_for_task(self, task):
        return self.get_pre_final_stage_for_project(task.project_id)

    @api.model
    def get_final_stage_for_task(self, task):
        return self.get_final_stage_for_project(task.project_id)

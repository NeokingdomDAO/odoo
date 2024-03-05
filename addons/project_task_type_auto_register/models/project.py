from odoo import api, fields, models

class Project(models.Model):
    _inherit = 'project.project'

    def register_to_all_stages(self):
        update_operations = [(4, project.id) for project in self]
        relevant_task_types_domain = [('active', '=', True), ('user_id', '=', False)]
        for stage in self.env['project.task.type'].search(relevant_task_types_domain):
            stage.write({'project_ids': update_operations})

    @api.model_create_multi
    def create(self, vals_list):
        projects = super().create(vals_list)
        projects.register_to_all_stages()
        return projects

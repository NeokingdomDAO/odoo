from odoo import fields, models

class Task(models.Model):
    _inherit = 'project.task'

    tag_ids = fields.Many2many('project.tags', required=True)
    date_deadline = fields.Date(required=True)

    def write(self, values):
        if values.get('parent_id', False):
            values['display_project_id'] = None
        return super().write(values)

# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    tag_ids = fields.Many2many(
        comodel_name='project.tags',
        required=True
    )
    date_deadline = fields.Date(
        required=True,
        default=lambda self: fields.Date.today()
    )

    def write(self, values):
        if values.get('parent_id', False):
            values['display_project_id'] = None
        return super().write(values)

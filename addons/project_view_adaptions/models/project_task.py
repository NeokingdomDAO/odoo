# -*- coding: utf-8 -*-

from odoo import fields, models, api


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
    contributing_users = fields.Many2many('res.users', string='Contributing Users', compute='_compute_contributing_users', store=True, readonly=True)

    @api.depends('user_ids', 'approval_user_id')
    def _compute_contributing_users(self):
        for _task in self:
            # controller is always a contributing user
            if _task.approval_user_id.exists():
                _contributing_users = {_task.approval_user_id.id}
            else:
                _contributing_users = {}

            # add task assignees also as contributors
            _contributing_users.update(_task.user_ids.ids)

            _task.contributing_users = [(6, 0, list(_contributing_users))]

    def write(self, values):
        if values.get('parent_id', False):
            values['display_project_id'] = None
        return super().write(values)

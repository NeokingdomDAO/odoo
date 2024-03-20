# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    tag_ids = fields.Many2many(
        comodel_name='project.tags',
        required=True
    )
    date_deadline = fields.Date(
        required=True,
        default=lambda self: fields.Date.today()
    )
    contributing_users = fields.Many2many('res.users', string='Contributing Users', compute='_compute_contributing_users', store=True, readonly=True)

    @api.depends('user_id', 'task_ids')
    def _compute_contributing_users(self):
        for _project in self:
            # project manager is always a contributing user
            _contributing_users = {_project.user_id.id}

            # add task assignees also as contributors
            for task in _project.task_ids:
                _contributing_users.update(task.user_ids.ids)

            _project.contributing_users = [(6, 0, list(_contributing_users))]

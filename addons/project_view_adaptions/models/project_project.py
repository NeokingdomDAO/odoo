# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    tag_ids = fields.Many2many(
        comodel_name='project.tags',
        required=True,
        tracking=True
    )
    date_deadline = fields.Date(
        required=True,
        default=lambda self: fields.Date.today(),
        tracking=True
    )
    name = fields.Char(tracking=True)
    label_tasks = fields.Char(tracking=True)
    partner_id = fields.Many2one(tracking=True)
    date_start = fields.Date(tracking=True)
    date = fields.Date(tracking=True)
    allocated_hours = fields.Float(tracking=True)
    privacy_visibility = fields.Selection(tracking=True)
    allow_subtasks = fields.Boolean(tracking=True)
    allow_task_dependencies = fields.Boolean(tracking=True)
    allow_timesheets = fields.Boolean(tracking=True)
    contributing_users = fields.Many2many('res.users', string='Contributing Users', compute='_compute_contributing_users', store=True, readonly=True)

    def write(self, values):
        changing_desc = 'description' in values

        if changing_desc:
            # create id: old description dict
            old_desc = {_project.id: _project.description for _project in self}

        result = super().write(values)

        # "manually" post description change to messages, since tracking attributes cause html widget to stop working
        if changing_desc:
            for _project in self:
                _project.message_post(body='<p>Description changed</p><p>{0}</p><p>→</p><p>{1}</p>'.format(
                    old_desc.get(_project.id, ''), values["description"]
                ))

        return result

    @api.depends('user_id', 'task_ids')
    def _compute_contributing_users(self):
        for _project in self:
            # project manager is always a contributing user
            if _project.user_id.exists():
                _contributing_users = {_project.user_id.id}
            else:
                _contributing_users = set()

            # add task assignees also as contributors
            for task in _project.task_ids:
                _contributing_users.update(task.user_ids.ids)

            if len(_contributing_users):
                _project.contributing_users = [(6, 0, list(_contributing_users))]

# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


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

    def action_open_project(self):
        return {
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'context': self._context
        }

    def action_open_migrate_open_tasks_dialog(self):
        return {
            'name': 'Migrate open tasks from previous project',
            'type': 'ir.actions.act_window',
            'res_model': 'project.migrate.tasks.dialog',
            'view_mode': 'form',
            'target': 'new'
        }


class ProjectMigrateTasksDialog(models.TransientModel):
    _name = 'project.migrate.tasks.dialog'
    _description = 'Migrate Project Tasks Dialog'

    prev_project_id = fields.Many2one('project.project', string='Previous Project', required=True)
    task_ids = fields.Many2many('project.task', string='Tasks to migrate', required=True)

    @api.onchange('prev_project_id')
    def _onchange_prev_project_id(self):
        self.task_ids = self.env['project.task'].search([
            ('project_id', '=', self.prev_project_id.id), ('stage_id.stage_type', 'not in', ['final', 'pre_final'])
        ])

    def action_migrate_open_tasks(self):
        active_model = self._context.get('active_model')
        active_id = self._context.get('active_id')
        opened_project = self.env[active_model].browse(active_id)

        if not active_model or not active_id or not opened_project.exists():
            return ValidationError('Migration failed.. Contact your system administrator.')

        for task in self.task_ids:
            task.write({'project_id': opened_project.id})

        return {'type': 'ir.actions.act_window_close'}

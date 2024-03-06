# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

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
    contributing_users = fields.Many2many('res.users', string='Contributing Users', compute='_compute_contributing_users', store=True, readonly=True)
    stage_id = fields.Many2one(tracking=True)
    name = fields.Char(tracking=True)
    project_id = fields.Many2one(tracking=True)
    date_deadline = fields.Date(tracking=True)
    user_ids = fields.Many2many(tracking=True)
    planned_hours = fields.Float(tracking=True)
    partner_id = fields.Many2one(tracking=True)
    sequence = fields.Integer(tracking=True)
    email_cc = fields.Char(tracking=True)
    timesheet_ids = fields.One2many(tracking=True)
    child_ids = fields.One2many(tracking=True)

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
        changing_desc = 'description' in values

        if changing_desc:
            # create id: old description dict
            old_desc = {_task.id: _task.description for _task in self}

        if values.get('parent_id', False):
            values['display_project_id'] = None

        res = super().write(values)

        # "manually" post description change to messages, since tracking attributes cause html widget to stop working
        if changing_desc:
            for _task in self:
                _task.message_post(body='<p>Description changed</p><p>{0}</p><p>→</p><p>{1}</p>'.format(
                    old_desc.get(_task.id, ''), values["description"]
                ))

        return res

    def action_create_pub_link(self):
        return {
            'name': 'Create publicly shareable link',
            'type': 'ir.actions.act_window',
            'res_model': 'portal.share',
            'view_mode': 'form',
            'target': 'new'
        }

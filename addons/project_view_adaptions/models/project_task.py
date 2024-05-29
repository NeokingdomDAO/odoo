# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # try to find applicable stages based on project
        # to include columns (stages) even if they have no record assigned to
        _project_id = False
        applicable_stage_ids = False

        if domain:
            for _domain in domain:
                if _domain[0] == 'display_project_id':
                    _project_id = _domain[2]

        if _project_id:
            # use project specific stages to group
            applicable_stage_ids = self.env['project.task.type'].search([('project_ids', 'in', [_project_id])])
        else:
            # use the default stages to group
            applicable_stage_ids = self.env['project.task.type'].search([('default_stage_for_group', '=', True)])

        if applicable_stage_ids:
            stages = applicable_stage_ids

        return super(ProjectTask, self)._read_group_stage_ids(stages, domain, order)

    def _default_project_id(self):
        # if creating task inside a project
        # then fill the project field by default with the opened project
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')

        if not active_model or not active_id:
            return False

        return self.env[active_model].browse(active_id).id

    tag_ids = fields.Many2many(
        comodel_name='project.tags',
        required=False,
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
    project_id = fields.Many2one(tracking=True, required=True, default=_default_project_id)
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
                _contributing_users = set()

            # add task assignees also as contributors
            if _task.user_ids.exists():
                _contributing_users.update(_task.user_ids.ids)

                _task.contributing_users = [(6, 0, list(_contributing_users))]

    def _post_update_project_tags(self):
        # add task tags to project tags
        for _task in self:
            _project_tags = _task.project_id.tag_ids
            _changed = False

            for _tag in _task.tag_ids:
                if _tag.id not in _project_tags.ids:
                    _project_tags += _tag
                    _changed = True

            if _changed:
                _task.project_id.tag_ids = _project_tags

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

        self._post_update_project_tags()

        return res

    def action_create_pub_link(self):
        return {
            'name': 'Create publicly shareable link',
            'type': 'ir.actions.act_window',
            'res_model': 'portal.share',
            'view_mode': 'form',
            'target': 'new'
        }

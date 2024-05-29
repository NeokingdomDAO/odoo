# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    project_manager_id = fields.Many2one('res.users', string='Project Manager', related='project_id.user_id', store=True, readonly=True)

    def _post_update_project_tags(self):
        _circle_tags = self.env['project.tags'].search([('is_circle_tag', '=', True)]).ids

        # add task tags to project tags
        for _task in self:
            _project_tags = _task.project_id.project_tag_ids
            _project_circle_tags = _task.project_id.circle_tag_ids
            _changed_pt = False
            _changed_ct = False

            for _tag in _task.tag_ids:
                _in_circle_tags = _tag.id in _circle_tags

                if (_tag.id not in _project_tags.ids) and (not _in_circle_tags):
                    _project_tags += _tag
                    _changed_pt = True
                elif (_tag.id not in _project_circle_tags.ids) and _in_circle_tags:
                    _project_circle_tags += _tag
                    _changed_ct = True

            if _changed_pt:
                _task.project_id.project_tag_ids = _project_tags
            if _changed_ct:
                _task.project_id.circle_tag_ids = _project_circle_tags

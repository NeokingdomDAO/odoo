# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_tag_ids = fields.Many2many('project.tags', 'neok_project_tag_rel', string='Project Tags')
    circle_tag_ids = fields.Many2many('project.tags', 'neok_circle_tag_rel', string='Circle Tags')
    tag_ids = fields.Many2many(compute='_compute_tag_ids', store=True)

    @api.depends('project_tag_ids', 'circle_tag_ids')
    def _compute_tag_ids(self):
        for project in self:
            project.tag_ids = project.project_tag_ids | project.circle_tag_ids

    def action_add_all_circle_tags(self):
        self.ensure_one()

        self.circle_tag_ids = self.env['project.tags'].search([('is_circle_tag', '=', True)])

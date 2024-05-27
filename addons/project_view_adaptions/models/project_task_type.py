# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    default_stage_for_group = fields.Boolean('Default Stage for Group', default=False, help='If checked, this stage may used as default stage for groupping if no project found as a base.')

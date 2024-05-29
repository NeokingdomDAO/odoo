# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTags(models.Model):
    _inherit = 'project.tags'

    is_circle_tag = fields.Boolean('Is Circle Tag', default=False)

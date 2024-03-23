# -*- coding: utf-8 -*-
from odoo import models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def create(self, values):
        res = super().create(values)

        if isinstance(values, list):
            if any((att_val.get('res_model') == 'project.task') for att_val in values):
                res.add_img_attchment_as_task_cover_img()
        elif values.get('res_model') == 'project.task':
            res.add_img_attchment_as_task_cover_img()

        return res

    def add_img_attchment_as_task_cover_img(self):
        # if it's a task attachment, and it's an image add it as cover image
        for _att in self:
            _task = self.env['project.task'].browse(_att.res_id)

            if _task.exists() and not _task.displayed_image_id.exists() and _att.mimetype.startswith('image'):
                _task.displayed_image_id = _att.id

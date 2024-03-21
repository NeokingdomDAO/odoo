# -*- coding: utf-8 -*-
from odoo import models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def create(self, values):
        res = super().create(values)

        # if it's a task attachment, and it's an image add it as cover image
        if values.get('res_model') == 'project.task':
            _res_id = values.get('res_id', False)

            if _res_id:
                _task = self.env['project.task'].browse(_res_id)

                if _task.exists() and not _task.displayed_image_id.exists() and res.mimetype.startswith('image'):
                    _task.displayed_image_id = res.id

        return res

from odoo import models, api, fields, _
from odoo.exceptions import UserError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not all(active_flag for active_flag in records.mapped('task_id.active')):
            raise UserError(_('Creating time entries on archived tasks is not allowed!'))
        return records

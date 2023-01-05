from dateutil.relativedelta import relativedelta
from odoo import models, api, fields, _
from odoo.exceptions import UserError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    employee_id = fields.Many2one(required=True)
    task_id = fields.Many2one(required=True)

    @api.constrains('task_id.user_ids')
    def check_no_time_tracked(self):
        raise UserError(_("You cannot reassign a task after time has been tracked!"))

    def search_overlapping_ids(self, date_criteria):
        self.ensure_one()
        day_after_start = self.date + relativedelta(days=1)
        search_criteria = [('id', '!=', self.id), ('employee_id', '=', self.employee_id.id)]
        search_criteria.extend(date_criteria)
        return self.search(search_criteria)

    def check_not_overlapping(self):
        self.ensure_one()
        overlapping_ids_at_start = self.search_overlapping_ids([('start', '<=', self.start), ('end', '>', self.start)])
        overlapping_ids_at_end = self.search_overlapping_ids([('start', '<', self.end), ('end', '>=', self.end)])
        overlapping_ids = overlapping_ids_at_start + overlapping_ids_at_end
        if overlapping_ids.exists():
            raise UserError(_("Ensure that no timesheets are overlapping!"))

    @api.constrains('start', 'end', 'amount')
    def ensure_not_overlapping(self):
        for line in self.filtered(lambda line: line.start and line.end):
            line.check_not_overlapping()

    def write(self, values):
        if any(stage_id.is_final() for stage_id in self.mapped('task_id.stage_id')):
            raise UserError(_("After a task is approved you are not allowed to change values of the timesheet!"))
        return super().write(values)

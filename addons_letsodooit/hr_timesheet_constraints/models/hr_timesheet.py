from dateutil.relativedelta import relativedelta
from odoo import models, api, fields, _
from odoo.exceptions import UserError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    employee_id = fields.Many2one(required=True)
    task_id = fields.Many2one(required=True)

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

    @api.constrains('task_id')
    def ensure_employee_part_of_assignees(self):
        for line in self:
            line.task_id.ensure_employee_part_of_assignees()

    @api.model
    def _sanitize_start_and_end(self, values):
        def zero_seconds(date_string):
            return fields.Datetime.from_string(date_string).replace(second=0, microsecond=0)
        if values.get('start', False):
            values['start'] = zero_seconds(values['start'])
        if values.get('end', False):
            values['end'] = zero_seconds(values['end'])

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            self._sanitize_start_and_end(values)
        return super().create(vals_list)

    def write(self, values):
        if any(stage_id.is_final() for stage_id in self.mapped('task_id.stage_id')):
            raise UserError(_("After a task is approved you are not allowed to change values of the timesheet!"))
        self._sanitize_start_and_end(values)
        return super().write(values)

    def unlink(self):
        if any(stage_id.is_final() for stage_id in self.mapped('task_id.stage_id')):
            raise UserError(_("After a task is approved you are not allowed to delete a timesheet!"))
        return super().unlink()

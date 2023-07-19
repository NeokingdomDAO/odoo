from dateutil.relativedelta import relativedelta
from odoo import models, api, fields, _
from odoo.osv import expression
from odoo.exceptions import UserError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    employee_id = fields.Many2one(required=True)
    task_id = fields.Many2one(required=True)

    def search_extended(self, search_criteria):
        self.ensure_one()
        search_criteria_extension = [('id', '!=', self.id), ('employee_id', '=', self.employee_id.id)]
        search_criteria = expression.AND([search_criteria, search_criteria_extension])
        return self.search(search_criteria)

    def _add_first_case_to_error_message(self, error_message, overlapping_line_ids):
        overlapping_line_id = overlapping_line_ids[0]
        description = overlapping_line_id.name
        task_name = overlapping_line_id.task_id.name
        return error_message + _("\n\nCollision with timesheet '{}' on task '{}'.".format(description, task_name))

    def check_start_not_overlapping(self):
        self.ensure_one()
        overlapping_line_ids = self.search_extended([
            ('start', '<=', self.start),
            ('end', '>', self.start)
        ])
        if overlapping_line_ids:
            error_message = _('The start of your timesheet is overlapping!')
            raise UserError(self._add_first_case_to_error_message(error_message, overlapping_line_ids))

    def check_end_not_overlapping(self):
        self.ensure_one()
        overlapping_line_ids = self.search_extended([
            ('start', '<', self.end),
            ('end', '>=', self.end)
        ])
        if overlapping_line_ids:
            error_message = _('The end of your timesheet is overlapping!')
            raise UserError(self._add_first_case_to_error_message(error_message, overlapping_line_ids))

    def check_not_surrounding(self):
        self.ensure_one()
        overlapping_line_ids = self.search_extended([
            ('start', '>=', self.start),
            ('end', '<=', self.end)
        ])
        if overlapping_line_ids:
            error_message = _('Your timesheet is surrounding another one!')
            raise UserError(self._add_first_case_to_error_message(error_message, overlapping_line_ids))

    def check_only_open_line(self):
        self.ensure_one()
        overlapping_line_ids = self.search_extended([
            ('end', '=', False)
        ])
        if overlapping_line_ids:
            error_message = _('Only one timesheet is allowed to be open ended!')
            raise UserError(self._add_first_case_to_error_message(error_message, overlapping_line_ids))

    def check_user_is_allowed(self):
        current_employee = self.env['hr.employee'].search([
            ('user_id', '=', self.env.user.id)
        ], limit=1)
        if any(employee != current_employee for employee in self.employee_id):
            raise UserError(_("You are not allowed to create/edit/delete timesheets for other users!"))

    def check_not_final_stage(self):
        if any(stage_id.is_final() for stage_id in self.task_id.stage_id):
            raise UserError(_("After a task is approved you are not allowed to edit/delete a timesheet!"))

    @api.constrains('start', 'end')
    def ensure_not_overlapping(self):
        for line in self:
            line.check_start_not_overlapping()
            if line.end:
                line.check_end_not_overlapping()
                line.check_not_surrounding()
            else:
                line.check_only_open_line()

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
        records = super().create(vals_list)
        records.check_user_is_allowed()
        return records

    def write(self, values):
        self.check_user_is_allowed()
        self.check_not_final_stage()
        self._sanitize_start_and_end(values)
        return super().write(values)

    def unlink(self):
        self.check_user_is_allowed()
        self.check_not_final_stage()
        return super().unlink()

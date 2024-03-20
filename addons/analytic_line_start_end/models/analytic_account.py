from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    start = fields.Datetime(string='Start', required=True)
    end = fields.Datetime(string='End')
    date = fields.Date(
        string='Date',
        compute='_compute_date',
        store=True
    )
    unit_amount = fields.Float(
        string='Quantity',
        compute='_compute_unit_amount',
        default=0.0,
        store=True
    )

    @api.constrains('start', 'end')
    def ensure_start_before_end(self):
        for line in self.filtered(lambda line: line.start and line.end):
            if line.start > line.end:
                raise UserError(_('Start datetime must be before end datetime!'))

    @api.depends('start')
    def _compute_date(self):
        for line in self:
            line.date = line.start.date() if line.start else False

    @api.depends('start', 'end')
    def _compute_unit_amount(self):
        for line in self:
            line.unit_amount = 0.0
            if line.start and line.end:
                line.unit_amount = (line.end - line.start).total_seconds() / 3600.0

    @api.model
    def _sanitize_date_values(self, values):
        if 'date' in values and not 'start' in values:
            values['start'] = values['date']
            del values['date']

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            self._sanitize_date_values(values)
        return super().create(vals_list)

    def write(self, values):
        self._sanitize_date_values(values)
        return super().write(values)

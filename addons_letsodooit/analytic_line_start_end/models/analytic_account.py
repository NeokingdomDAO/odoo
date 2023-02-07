from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    start = fields.Datetime(string='Start', required=True)
    end = fields.Datetime(string='End')
    date = fields.Datetime(
        string='Date',
        compute='_compute_date',
        inverse='_inverse_date',
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

    def _inverse_date(self):
        for line in self:
            line.start = line.date

    @api.depends('start', 'end')
    def _compute_unit_amount(self):
        for line in self:
            line.unit_amount = 0.0
            if line.start and line.end:
                line.unit_amount = (line.end - line.start).total_seconds() / 3600.0

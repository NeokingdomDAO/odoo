# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _default_date_deadline(self):
        # if the project's deadline is set and its in this month, then we use that as its close
        # else we set the last day of the month to complete the task before the minting period
        if self.project_id.date_deadline and self.project_id.date_deadline.month == fields.Date.today().month:
            return self.project_id.date_deadline
        else:
            last_day_of_month = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            return last_day_of_month.date()

    date_deadline = fields.Date(
        default=_default_date_deadline,
    )

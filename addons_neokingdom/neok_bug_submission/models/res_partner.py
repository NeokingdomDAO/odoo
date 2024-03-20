# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    bug_submission_ids = fields.One2many('neok.helpdesk.bug.submission', 'partner_id', string='Bug Submissions')
    bug_submission_count = fields.Integer('Reported Issues', compute='_compute_bug_submission_count')

    def _compute_bug_submission_count(self):
        for _partner in self:
            _partner.bug_submission_count = len(_partner.bug_submission_ids)

    def action_view_bug_submissions(self):
        action = self.env['ir.actions.act_window']._for_xml_id('neok_bug_submission.bug_submission_action')
        action['domain'] = [('partner_id', '=', self.id)]

        return action

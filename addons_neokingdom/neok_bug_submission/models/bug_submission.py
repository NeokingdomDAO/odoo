# -*- coding: utf-8 -*-
import random
import string

from odoo import fields, models


class BugSubmission(models.Model):
    _name = 'neok.helpdesk.bug.submission'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = 'Bug Submission'
    _order = 'sequence desc'

    def _get_default_5_digit_sequence(self):
        # Ensure at least 3 digits are included
        digits = ''.join(random.choice(string.digits.replace('0', '')) for _ in range(3))

        # The remaining characters are uppercase letters excluding 'O'
        characters = string.ascii_uppercase.replace('O', '')

        # Combine digits and uppercase letters
        sequence = digits + ''.join(random.choice(characters) for _ in range(3))

        # Shuffle the sequence to make it random
        sequence_list = list(sequence)
        random.shuffle(sequence_list)

        return ''.join(sequence_list)

    sequence = fields.Integer()
    name = fields.Char(string='Name', default=_get_default_5_digit_sequence, readonly=True)
    title = fields.Char(string='Title', required=True, readonly=True)
    description = fields.Text(string='Description', required=False, readonly=True)
    dao_name = fields.Char(string='DAO Name', required=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, readonly=True)
    sender_email = fields.Char(related='partner_id.email', readonly=True)
    state = fields.Selection(
        [('received', 'Received'), ('done', 'Done'), ('irrelevant', 'Irrelevant')],
        string='State', default='received', readonly=False
    )
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', readonly=True)

    def action_done(self):
        for subm in self:
            subm.write({'state': 'done'})

    def action_irrelevant(self):
        for subm in self:
            subm.write({'state': 'irrelevant'})

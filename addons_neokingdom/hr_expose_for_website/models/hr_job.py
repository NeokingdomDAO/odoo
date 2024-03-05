# -*- coding: utf-8 -*-

from odoo import fields, models


class Job(models.Model):
    _inherit = 'hr.job'

    website_published = fields.Boolean(help='Set if the application is published on the website of the company.')
    website_url = fields.Char(compute='_compute_website_url', string='Website URL', help='The full URL to access the document through the website.')

    def _compute_website_url(self):
        for job in self:
            job.website_url = "https://www.neokingdom.org/apply/details/%s" % job.id

    def open_website_url(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.website_url,
            'target': 'new',
        }

    def set_open(self):
        self.write({'website_published': False})
        return super(Job, self).set_open()

    def toggle_active(self):
        self.filtered('active').website_published = False
        return super().toggle_active()

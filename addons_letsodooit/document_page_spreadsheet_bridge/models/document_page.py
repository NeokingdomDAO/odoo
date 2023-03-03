from odoo import models

class DocumentPage(models.Model):
    _name = "document.page"
    _inherit = ["document.page", "spreadsheet.abstract"]

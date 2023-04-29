from odoo import api, fields, models, _

class Task(models.Model):
    _inherit = 'project.task'

    @api.model
    def _get_default_tier_id(self):
        tier_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1).tier_id
        if not tier_id:
            tier_id = self.env['account.analytic.tier'].create({'name': 'Basic'})
        return tier_id

    tier_id = fields.Many2one(
        comodel_name='account.analytic.tier',
        string='Tier',
        required=True,
        default=_get_default_tier_id
    )

    @api.onchange('user_ids')
    def onchange_user_ids(self):
        employee_ids = self.env['hr.employee'].search([('user_id', 'in', self.user_ids.ids)])
        if employee_ids:
            possible_tiers = employee_ids.tier_id
            if possible_tiers:
                self.tier_id = possible_tiers[0]

import ast

from odoo import api, models


class NeokPotProjectTask(models.Model):
    _inherit = 'project.task'

    def read(self, fields=None, load='_classic_read'):
        # if the returned list length is 1, then its most likely a form open read
        if not self._context.get('from_web_search_read', False) and len(self) == 1:
            self.env['neok.pot.history'].sudo().create({
                'task_id': self.id,
                'user_id': self.env.user.id,
            })

        return super(NeokPotProjectTask, self).read(fields=fields, load=load)

    @api.model
    def get_previously_opened_10_tasks(self):
        # @TODO: colors can be extracted from tags to further improve ui elements
        _tasks = self.env['neok.pot.history'].sudo().search([('user_id', '=', self.env.user.id)], order='write_date desc')

        return [{
            'id': task.id,
            'name': task.name,
        } for task in _tasks.mapped('task_id')]

    @api.model
    def get_pot_viable_ids(self):
        if not self.env.user.show_pot:
            return []

        return ast.literal_eval(self.env['ir.config_parameter'].sudo().get_param('neok_pot_viable_action_ids', '[]'))

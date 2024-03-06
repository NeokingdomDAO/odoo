from odoo import api, fields, models


class NeokPotHistory(models.Model):
    _name = 'neok.pot.history'

    task_id = fields.Many2one('project.task', string='Task')
    user_id = fields.Many2one('res.users', string='User')

    def create(self, vals_list):
        user_history = self.search([('user_id', '=', self.env.user.id)], order='write_date')

        if 'task_id' not in vals_list:
            return
        elif vals_list['task_id'] in user_history.mapped('task_id').ids:
            # if opened task is already in the history, update create_date field to now
            task_to_edit = user_history.filtered(lambda x: x.task_id.id == vals_list['task_id'])
            task_to_edit.write({'write_date': fields.Datetime.now()})
            return

        self._shift_pot_history(user_history)
        return super(NeokPotHistory, self).create(vals_list)

    def _shift_pot_history(self, user_history):
        # if the user has more than 10 records, then delete the oldest one
        if len(user_history) >= 10:
            user_history[0].unlink()

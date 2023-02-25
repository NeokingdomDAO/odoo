from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Task(models.Model):
    _inherit = 'project.task'

    user_id = fields.Many2one('res.users', string='Assignee', required=True, tracking=True)
    user_ids = fields.Many2many('res.users', compute='_compute_user_ids', inverse='_inverse_user_ids', store=True)
    is_approval_stage = fields.Boolean('Is Approval Stage', compute='_compute_is_approval_stage', store=True)
    approval_user_id = fields.Many2one('res.users', string='Controller', required=True, tracking=True)
    approval_date = fields.Date(string='Approval Date', readonly=True)

    @api.constrains('user_id', 'approval_user_id')
    def check_user_and_approval_user_not_equal(self):
        for task in self:
            if task.user_id == task.approval_user_id:
                raise UserError(_('Please ensure that the assignee is not the controller.'))

    @api.depends('user_id')
    def _compute_user_ids(self):
        for task in self:
            task.user_ids = task.user_id

    def _inverse_user_ids(self):
        for task in self:
            task.user_id = task.user_ids[0] if task.user_ids else False

    @api.depends('stage_id')
    def _compute_is_approval_stage(self):
        for task in self:
            task.is_approval_stage = task.stage_id.is_pre_final()

    def action_approve(self):
        for task in self:
            if self.env.user != task.approval_user_id:
                raise UserError(_('You are not the approver of this tasks. You are not allowed to perform this action!'))
            final_stage = self.env['project.task.type'].get_final_stage_for_task(task)
            task.with_context(force_final_stage=True).write({
                'stage_id': final_stage.id,
                'approval_date': fields.Date.today()
            })

    def write(self, values):
        result = super().write(values)
        for record in self:
            if record.stage_id.is_final() and not self.env.context.get('force_final_stage', False):
                raise UserError(_('Please use the approve button to set a task to approved!'))
            if record.is_approval_stage:
                activity_values = {
                    'act_type_xmlid': 'project_task_approval.mail_activity_data_approval',
                    'summary': _('Please approve the task!'),
                    'note': _('A task you have been assigned for as controller has reached the approval stage!'),
                    'user_id': record.approval_user_id.id
                }
                record.activity_schedule(**activity_values)
            else:
                record.activity_unlink(['project_task_approval.mail_activity_data_approval'])
        return result

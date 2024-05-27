from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Task(models.Model):
    _inherit = 'project.task'

    # ! user_id is no deprecated, kept here to hold old data, use user_ids instead !
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assignee',
        required=False,
        tracking=False
    )
    is_approval_stage = fields.Boolean(
        string='Is Approval Stage',
        compute='_compute_is_approval_stage',
        store=True
    )
    approval_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Controller',
        tracking=True,
        required=False
    )
    approval_date = fields.Date(
        string='Approval Date',
        readonly=True
    )

    @api.constrains('user_ids', 'approval_user_id')
    def check_user_and_approval_user_not_equal(self):
        for task in self:
            if task.approval_user_id in task.user_ids:
                raise UserError(_('Please ensure the assignee and controller are not the same.'))

    @api.constrains('stage_id')
    def check_approval_user_id_set(self):
        for task in self:
            if task.is_approval_stage and not task.approval_user_id:
                raise UserError(_('Please ensure that a controller is set when the task is in approval stage.'))

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
                if not record.activity_search(act_type_xmlids=['project_task_approval.mail_activity_data_approval']):
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

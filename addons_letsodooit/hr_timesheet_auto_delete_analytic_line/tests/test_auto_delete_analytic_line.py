from odoo.exceptions import UserError
from odoo.tests import common

class TestAutoDeleteAnalyticLine(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.user_id = self.env['res.users'].create({
            'name': 'User',
            'login': 'Login'
        })
        self.employee_id = self.env['hr.employee'].create({
            'user_id': self.user_id.id
        })
        self.project_id = self.env['project.project'].create({
            'name': 'Project'
        })
        self.task_id = self.env['project.task'].create({
            'name': 'Task',
            'project_id': self.project_id.id,
            'user_ids': self.user_id
        })


    def test_auto_deletion_create(self):
        return
        #TODO: fix when multi assignees are possible!
        task_id = self.env['project.task'].create({
            'active': False,
            'name': 'Task',
            'project_id': self.project_id.id,
            'user_ids': self.user_id,
            'timesheet_ids': [(0, 0, {
                'employee_id': self.employee_id.id,
                'date': '2022-01-01'
            })]
        })
        self.assertFalse(self.env['account.analytic.line'].search([('task_id', '=', task_id.id)]))

    def test_auto_deletion_write(self):
        record = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'date': '2022-01-01'
        })
        self.task_id.write({'active': False})
        self.env.invalidate_all()
        self.assertFalse(record.exists())

    def test_auto_deletion_archive(self):
        record = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'date': '2022-01-01'
        })
        self.task_id.action_archive()
        self.assertFalse(record.exists())

    def test_auto_deletion_create_on_archived_task(self):
        self.task_id.action_archive()
        with self.assertRaises(UserError):
            record = self.env['account.analytic.line'].create({
                'project_id': self.project_id.id,
                'task_id': self.task_id.id,
                'employee_id': self.employee_id.id,
                'date': '2022-01-01'
            })

    def test_no_auto_deletion(self):
        record = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'date': '2022-01-01'
        })
        with self.assertRaises(Exception):
            self.task_id.unlink()

from odoo.tests import common
from odoo.exceptions import UserError

class TestHRTimesheetConstraints(common.TransactionCase):
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
        self.timesheet_id = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'start': '2022-01-01',
            'end': '2022-01-10'
        })

    def test_no_multi_open_end_create(self):
        self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'start': '2023-01-01'
        })
        with self.assertRaises(UserError):
            self.env['account.analytic.line'].create({
                'project_id': self.project_id.id,
                'task_id': self.task_id.id,
                'employee_id': self.employee_id.id,
                'start': '2023-02-01'
            })

    def test_no_multi_open_end_write(self):
        self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'start': '2023-01-01'
        })
        timesheet_id = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'start': '2023-01-01',
            'end': '2023-01-02'
        })
        with self.assertRaises(UserError):
            timesheet_id.write({'end': False})

    def test_no_start_date_overlapping_create(self):
        with self.assertRaises(UserError):
            self.env['account.analytic.line'].create({
                'project_id': self.project_id.id,
                'task_id': self.task_id.id,
                'employee_id': self.employee_id.id,
                'start': '2022-01-01'
            })

    def test_no_start_date_overlapping_write(self):
        timesheet_id = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'start': '2023-01-01'
        })
        with self.assertRaises(UserError):
            timesheet_id.write({'start': '2022-01-01'})

    def test_no_end_date_overlapping_create(self):
        with self.assertRaises(UserError):
            self.env['account.analytic.line'].create({
                'project_id': self.project_id.id,
                'task_id': self.task_id.id,
                'employee_id': self.employee_id.id,
                'start': '2021-01-01',
                'end': '2022-01-02'
            })

    def test_no_end_date_overlapping_write(self):
        timesheet_id = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'start': '2021-01-01',
            'end': '2022-01-01'
        })
        with self.assertRaises(UserError):
            timesheet_id.write({'end': '2022-01-02'})

    def test_no_surrounding_timesheet_overlapping_create(self):
        with self.assertRaises(UserError):
            self.env['account.analytic.line'].create({
                'project_id': self.project_id.id,
                'task_id': self.task_id.id,
                'employee_id': self.employee_id.id,
                'start': '2021-01-01',
                'end': '2022-01-09'
            })

    def test_is_not_surrounding_create(self):
        with self.assertRaises(UserError):
            self.env['account.analytic.line'].create({
                'project_id': self.project_id.id,
                'task_id': self.task_id.id,
                'employee_id': self.employee_id.id,
                'start': '2021-01-01',
                'end': '2022-01-20'
            })
        
    def test_is_not_surrounding_write_start(self):
        timesheet_id = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'start': '2022-01-20',
            'end': '2022-01-30'
        })
        with self.assertRaises(UserError):
            timesheet_id.write({'start': '2021-01-01'})

    def test_is_not_surrounding_write_end(self):
        timesheet_id = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'start': '2021-01-01',
            'end': '2022-01-01'
        })
        with self.assertRaises(UserError):
            timesheet_id.write({'end': '2022-01-20'})

    def test_all_good(self):
        timesheet_id = self.env['account.analytic.line'].create({
            'project_id': self.project_id.id,
            'task_id': self.task_id.id,
            'employee_id': self.employee_id.id,
            'start': '2023-01-01',
            'end': '2023-01-02'
        })

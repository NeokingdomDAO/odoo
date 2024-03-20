from odoo.tests import common
from odoo.exceptions import UserError


class TestProjectContraints(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.project = self.env['project.project'].create({
            'name': 'Project',
        })
        self.initial_project_task_type = self.env['project.task.type'].create({
            'name': 'Initial',
            'sequence': 1,
            'stage_type': 'initial',
            'project_ids': self.project
        })
        self.final_project_task_type = self.env['project.task.type'].create({
            'name': 'Final',
            'sequence': 2,
            'stage_type': 'final',
            'project_ids': self.project
        })
        self.task = self.env['project.task'].create({
            'name': 'Task',
            'project_id': self.project.id
        })

    def test_project_task_type_final_no_change(self):
        self.task.with_context(force_final_stage=True).write({'stage_id': self.final_project_task_type.id})
        with self.assertRaises(UserError):
            self.task.write({'name': 'Task2'})

    def test_project_task_type_final_no_delete(self):
        self.task.with_context(force_final_stage=True).write({'stage_id': self.final_project_task_type.id})
        with self.assertRaises(UserError):
            self.task.unlink()

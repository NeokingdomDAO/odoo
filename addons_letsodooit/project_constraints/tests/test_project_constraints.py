from odoo.tests import common
from odoo.exceptions import UserError


class TestProjectContraints(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.final_project_task_type_id = self.env['project.task.type'].create({
            'name': 'Final',
            'stage_type': 'final'
        })
        self.project_id = self.env['project.project'].create({
            'name': 'Project',
            'type_ids': self.final_project_task_type_id
        })
        self.task_id = self.env['project.task'].create({
            'name': 'Task',
            'project_id': self.project_id.id
        })

    def test_project_task_type_final_no_change(self):
        self.task_id.with_context(force_final_stage=True).write({'stage_id': self.final_project_task_type_id.id})
        with self.assertRaises(UserError):
            self.task_id.write({'name': 'Task2'})

    def test_project_task_type_final_no_delete(self):
        self.task_id.with_context(force_final_stage=True).write({'stage_id': self.final_project_task_type_id.id})
        with self.assertRaises(UserError):
            self.task_id.unlink()

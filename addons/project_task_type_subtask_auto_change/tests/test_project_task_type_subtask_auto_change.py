from odoo.tests import common
from odoo.exceptions import UserError

class TestProjectTaskTypeSubtaskAutoChange(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.user_id = self.env['res.users'].create({
            'name': 'User',
            'login': 'Login'
        })
        self.project_id = self.env['project.project'].create({
            'name': 'Project'
        })
        ProjectTaskType = self.env['project.task.type']
        self.first_stage = ProjectTaskType.create({
            'sequence': 1,
            'name': 'First',
            'subtask_criterion': 'any',
            'project_ids': self.project_id
        })
        self.second_stage = ProjectTaskType.create({
            'sequence': 2,
            'name': 'Second',
            'subtask_criterion': 'any',
            'project_ids': self.project_id
        })
        self.third_stage = ProjectTaskType.create({
            'sequence': 3,
            'name': 'Third',
            'subtask_criterion': 'all',
            'ignore_task_rule_domain': "[('name', '=', 'Tas')]",
            'project_ids': self.project_id
        })
        self.fourth_stage = ProjectTaskType.create({
            'sequence': 4,
            'name': 'Fourth',
            'subtask_criterion': 'all',
            'ignore_task_rule_domain': "[('name', '=', 'Task')]",
            'project_ids': self.project_id
        })
        self.subtask_1 = self.task_id = self.env['project.task'].create({
            'name': 'Subtask 1',
            'project_id': self.project_id.id,
        })
        self.subtask_2 = self.task_id = self.env['project.task'].create({
            'name': 'Subtask 2',
            'project_id': self.project_id.id,
        })
        self.task = self.env['project.task'].create({
            'name': 'Task',
            'project_id': self.project_id.id,
            'child_ids': self.subtask_1 + self.subtask_2
        })

    def test_first_stage(self):
        self.assertEqual(self.subtask_1.stage_id, self.first_stage)
        self.assertEqual(self.subtask_2.stage_id, self.first_stage)
        self.assertEqual(self.task.stage_id, self.first_stage)

    def test_second_stage(self):
        self.subtask_1.write({'stage_id': self.second_stage.id})
        self.assertEqual(self.subtask_1.stage_id, self.second_stage)
        self.assertEqual(self.subtask_2.stage_id, self.first_stage)
        self.assertEqual(self.task.stage_id, self.second_stage)

    def test_third_stage(self):
        self.subtask_1.write({'stage_id': self.third_stage.id})
        self.assertEqual(self.subtask_1.stage_id, self.third_stage)
        self.assertEqual(self.subtask_2.stage_id, self.first_stage)
        self.assertEqual(self.task.stage_id, self.second_stage)
        self.subtask_2.write({'stage_id': self.third_stage.id})
        self.assertEqual(self.subtask_1.stage_id, self.third_stage)
        self.assertEqual(self.subtask_2.stage_id, self.third_stage)
        self.assertEqual(self.task.stage_id, self.third_stage)
        self.subtask_2.write({'stage_id': self.second_stage.id})
        self.assertEqual(self.task.stage_id, self.second_stage)
        self.task.write({'name': 'Tas'})
        self.subtask_2.write({'stage_id': self.third_stage.id})
        self.assertEqual(self.subtask_2.stage_id, self.third_stage)
        self.assertEqual(self.task.stage_id, self.second_stage)
        self.task.write({'stage_id': self.third_stage.id})
        self.assertEqual(self.task.stage_id, self.third_stage)

    def test_fourth_stage(self):
        self.subtask_1.write({'stage_id': self.fourth_stage.id})
        self.assertEqual(self.subtask_1.stage_id, self.fourth_stage)
        self.assertEqual(self.subtask_2.stage_id, self.first_stage)
        self.assertEqual(self.task.stage_id, self.second_stage)
        self.subtask_2.write({'stage_id': self.fourth_stage.id})
        self.assertEqual(self.subtask_2.stage_id, self.fourth_stage)
        self.assertEqual(self.task.stage_id, self.third_stage)
        self.task.write({'stage_id': self.fourth_stage.id})
        self.assertEqual(self.task.stage_id, self.fourth_stage)
        self.task.write({'name': 'Ta'})
        self.subtask_2.write({'stage_id': self.third_stage.id})
        self.assertEqual(self.task.stage_id, self.third_stage)
        self.subtask_2.write({'stage_id': self.fourth_stage.id})
        self.assertEqual(self.task.stage_id, self.fourth_stage)

# -*- coding: utf-8 -*-
{
    'name': 'Project Views Adaptions',
    'version': '16.0.1.0.0',
    'sequence': 30,
    'category': 'NEOKingdom',
    'author': 'NEOKingdom Odoo Team (https://www.neokingdom.org)',
    'description': """This module adapts the views of project module to align with NEOCommonwealth instances.""",
    'depends': [
        'portal',
        'project',
        'project_task_approval'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/action.xml',
        'views/menu.xml',
        'views/project_migrate_tasks_dialog.xml',
        'views/project_project.xml',
        'views/project_task.xml',
        'views/project_task_type.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'project_view_adaptions/static/src/scss/project.scss',
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

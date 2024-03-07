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
        'views/action.xml',
        'views/menu.xml',
        'views/project_project.xml',
        'views/project_task.xml',
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

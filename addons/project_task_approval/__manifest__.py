{
    'name': 'Project Task Approval',
    'version': '16.0.1.0.0',
    'sequence': 1,
    'category': 'NEOKingdom',
    'author': 'NEOKingdom Odoo Team (https://www.neokingdom.org)',
    'description': """This module provides an approval process for project tasks.""",
    'depends': [
        'project',
        'project_task_type_attribution'
    ],
    'data': [
        'data/mail_activity_data.xml',
        'views/project_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

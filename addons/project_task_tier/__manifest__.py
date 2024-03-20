{
    'name': '(Deprecated) Project Task Tier',
    'version': '16.0.1.0.0',
    'sequence': 1,
    'category': 'NEOKingdom',
    'author': 'NEOKingdom Odoo Team (https://www.neokingdom.org)',
    'description': """(Deprecated) This module adds tiers to project tasks.""",
    'depends': [
        'project',
        'project_task_approval',
        'analytic_tier',
        'analytic_tier_hr_employee'
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

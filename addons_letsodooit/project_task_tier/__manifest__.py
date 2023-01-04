{
    'name' : 'Project Task Tier',
    'version' : '16.0.1.0.0',
    'author': 'Peter Schwarz (info@peter-schwarz.it)',
    'sequence': 1,
    'description': """This module adds tiers to project tasks.""",
    'license': 'OPL-1',
    'depends': ['project', 'project_task_approval', 'analytic_tier', 'analytic_tier_hr_employee'],
    'data': ['views/project_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}

{
    'name' : 'Project Task Approval',
    'version' : '16.0.1.0.0',
    'author': 'Peter Schwarz (info@peter-schwarz.it)',
    'sequence': 1,
    'description': """This module provides an approval process for project tasks.""",
    'license': 'OPL-1',
    'depends': ['project', 'project_task_type_attribution'],
    'data': ['views/project_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}

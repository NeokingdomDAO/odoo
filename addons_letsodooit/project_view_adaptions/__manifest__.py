{
    'name' : 'Project Views',
    'version' : '16.0.1.0.0',
    'author': 'Peter Schwarz (info@peter-schwarz.it)',
    'sequence': 1,
    'description': """This module adapts the project modules' views accordingly.""",
    'license': 'OPL-1',
    'depends': [
        'project',
        'project_task_approval'
    ],
    'data': [
        'views/project_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

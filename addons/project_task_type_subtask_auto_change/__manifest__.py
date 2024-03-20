{
    'name' : 'Project Task Type Subtask Auto Change',
    'version' : '16.0.1.0.0',
    'author': 'Peter Schwarz (info@peter-schwarz.it)',
    'sequence': 1,
    'description': """This module automatically changes a task's stage if its subtasks meet certain criteria.""",
    'license': 'OPL-1',
    'depends': ['project'],
    'data': ['views/project_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}

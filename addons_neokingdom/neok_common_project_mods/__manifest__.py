{
    'name': '(NEOKingdom) Common Project Management Modifications',
    'version': '16.0.1.0.0',
    'author': 'Bence Tóth (benhrisdev@gmail.com)',
    'category': 'NEOKindom',
    'sequence': 1,
    'description': """Contains modifications for the project management module, thats applicable to all neo-commonwealth projects.""",
    'license': 'OPL-1',
    'depends': ['base', 'project'],
    'data': [
        'views/project_project.xml',
        'views/project_task.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

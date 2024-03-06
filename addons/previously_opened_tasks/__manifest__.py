{
    'name': 'Previously Opened Tasks (Top Bar)',
    'version': '16.0.1.0.0',
    'sequence': 50,
    'category': 'NEOKingdom',
    'author': 'NEOKingdom Odoo Team (https://www.neokingdom.org)',
    'description': """Adds a top bar to the project management section, which displays the previously opened tasks.""",
    'depends': ['base', 'web', 'project', 'project_view_adaptions'],
    'data': [
        'security/ir.model.access.csv',
        'data/sys_param.xml',
        'views/res_user.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'previously_opened_tasks/static/src/views/kanban_renderer.xml',
            'previously_opened_tasks/static/src/js/kanban_renderer.js',
            'previously_opened_tasks/static/src/scss/kanban_renderer.scss',
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

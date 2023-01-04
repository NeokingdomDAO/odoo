{
    'name' : 'Analytic Tier (HR Employee)',
    'version' : '16.0.1.0.0',
    'author': 'Peter Schwarz',
    'sequence': 1,
    'description': """This module provides allows to set a tier on employees.""",
    'license': 'OPL-1',
    'depends': ['analytic_tier', 'hr'],
    'data': ['views/hr_employee_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}

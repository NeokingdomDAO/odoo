{
    'name' : 'HR Timesheet Views',
    'version' : '16.0.1.0.0',
    'author': 'Peter Schwarz (info@peter-schwarz.it)',
    'sequence': 1,
    'description': """This module adapts the hr timesheet modules' views accordingly.""",
    'license': 'OPL-1',
    'depends': ['hr_timesheet', 'analytic_line_start_end', 'analytic_tier'],
    'data': [
        'views/hr_timesheet_views.xml',
        'views/project_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

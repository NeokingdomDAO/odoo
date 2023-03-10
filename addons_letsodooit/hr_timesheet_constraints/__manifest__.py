{
    'name' : 'HR Timesheet Constraints',
    'version' : '16.0.1.0.0',
    'author': 'Peter Schwarz (info@peter-schwarz.it)',
    'sequence': 1,
    'description': """This module provides some basic constraints to HR timesheets to ensure data cleanness.""",
    'license': 'OPL-1',
    'depends': [
        'analytic_line_start_end',
        'hr_timesheet',
        'project_task_type_attribution'
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

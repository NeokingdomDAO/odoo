# -*- coding: utf-8 -*-
{
    'name': '(NEOKingdom) HR Expose for Website',
    'category': 'NEOKindom',
    'sequence': 20,
    'summary': 'HR Expose for Website as API.',
    'author': 'Bence Tóth (benhrisdev@gmail.com)',
    'description': "HR Expose for Website as API for dynamic rendering. DO NOT INSTALL ALONG WITH website_hr_recruitment!",
    'depends': ['base', 'hr', 'hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'security/website_hr_recruitment_security.xml',
        'views/hr_recruitment_views.xml',
        'views/hr_job_views.xml',
        'views/website_pages_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}

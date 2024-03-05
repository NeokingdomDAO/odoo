# -*- coding: utf-8 -*-
{
    'name': 'HR Expose for Website',
    'version': '16.0.1.0.0',
    'sequence': 20,
    'category': 'NEOKingdom',
    'author': 'NEOKingdom Odoo Team (https://www.neokingdom.org)',
    'description': "HR expose for NEOKingdom website as API for dynamic rendering. DO NOT INSTALL ALONG WITH website_hr_recruitment!",
    'depends': ['base', 'hr', 'hr_recruitment'],
    'data': [
        'security/ir.model.access.csv',
        'security/website_hr_recruitment_security.xml',
        'views/hr_recruitment_views.xml',
        'views/hr_job_views.xml',
        'views/website_pages_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}

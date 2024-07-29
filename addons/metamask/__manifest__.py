# -*- coding: utf-8 -*-
{
    'name': 'MetaMask Login',
    'version': '1.0',
    'summary': 'Login to Odoo using MetaMask Wallet',
    'description': 'Allows Odoo users to login using MetaMask Wallet',
    'category': 'Authentication',
    'author': 'Your Name',
    'depends': ['base', 'web'],
    'data': [
        'views/metamask_login_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/metamask/static/src/js/metamask_login.js'
        ],
    },
}

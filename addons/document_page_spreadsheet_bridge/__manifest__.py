{
    'name' : 'Document Page Spreadsheet Bridge',
    'version' : '16.0.1.0.0',
    'author': 'Peter Schwarz (info@peter-schwarz.it)',
    'sequence': 1,
    'description': """This module allows to do online editing on pages with spreadsheets.""",
    'license': 'OPL-1',
    'depends': [
        'document_page',
        'spreadsheet_oca'
    ],
    'data': [
        'views/document_page_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

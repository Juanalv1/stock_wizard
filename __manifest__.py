{
    'name': 'Stock Wizard',
    'version': '3.6',
    'category': 'Marketing/Surveys',
    'depends': ['base', 'stock', 'sale'],

    'data': [
        'security/ir.model.access.csv',
        'report/pdf_report_template.xml',
        'report/report.xml',
        'wizard/stock_wizard_view.xml',
        'views/stock_menu_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'stock_wizard/static/src/js/action_manager.js',
        ],
    },
    
    'installable': True,
    'application': True,
    'sequence': 220,
    'license': 'LGPL-3',
}

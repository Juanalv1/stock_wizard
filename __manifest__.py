{
    'name': 'Stock Wizard',
    'version': '3.6',
    'category': 'Marketing/Surveys',
    'depends': ['base', 'stock', 'sale'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_wizard.xml',
        'views/stock_menu_view.xml',

    ],
    'installable': True,
    'application': True,
    'sequence': 220,
    'license': 'LGPL-3',
}

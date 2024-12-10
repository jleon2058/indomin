{
    'name': """
        Custom Currency Rate on Invoices |
        Tipo de Cambio Personalizado en Facturas
    """,

    'summary': """
        
    """,

    'description': """
        
    """,

	'author': 'Develogers',
    'website': 'https://develogers.com',
    'support': 'especialistas@develogers.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'category': 'Localization',
    'version': '15.0',
    
    'price': 39.99,
    'currency': 'EUR',

    'depends': [
        'base',
        #'account',
        'dv_account_invoice_date_currency_rate',
        #'account_exchange_currency',
        #'payment_term_lines',
    ],

    'data': [
        'views/account_views.xml',
    ],

    'images': ['static/description/banner.gif'],

    'application': True,
    'installable': True,
    'auto_install': False,
}

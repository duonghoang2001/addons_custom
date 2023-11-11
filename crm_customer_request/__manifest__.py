# -*- coding: utf-8 -*-
{
    'name': "CRM Customer Request",

    'summary': """
        CRM Customer Request""",

    'description': """
        This module allows user to:
        - Add requests to opportunity manually or via Excel file (template provided), 
        - Export requests via Excel file,
        - Create quotation with inserted requests' data,
        - Create lead on API POST  HTTP request
    """,

    'author': "IZIsolution",

    'website': "https://izisolution.vn",

    'category': 'Assets',
    'version': '0.1',

    'depends': [
        'base', 
        'crm', 
        'sale_management', 
        'product',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'data': [
        'security/ir.model.access.csv',

        'views/crm_customer_request_views.xml',
        'views/crm_lead_views.xml',
        'views/product_set_views.xml',
        'views/crm_menu_views.xml'
    ],

    'assets': {
        'web.assets_backend' : [
            'crm_customer_request/static/src/js/utils.js',
            'crm_customer_request/static/src/js/todo.js',
            'crm_customer_request/static/src/js/todo_list.js',

            'crm_customer_request/static/src/xml/*',
        ],
        'web.asset_common' : [
            'web/static/src/libs/fontawesome/css/font-awesome.css', # required for fa icons
        ]
    },
}

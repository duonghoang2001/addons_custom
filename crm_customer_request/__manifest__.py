# -*- coding: utf-8 -*-
{
    'name': "CRM Customer Request",

    'summary': """
        CRM Customer Request Addon""",

    'description': """
        Allow user to add requests to a opportunity both manually and via Excel file, 
        and create quotation with inserted requests
    """,

    'author': "Duong Hoang",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 
        'crm', 
        'sale_management', 
        'product',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/crm_customer_request_views.xml',
        'views/crm_lead_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'license': 'LGPL-3',

    'application': True,
}

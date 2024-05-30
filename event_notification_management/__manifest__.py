# -*- coding: utf-8 -*-
{
    'name': "event notification management",
    'sequence' : -40,

    'summary': """
        notify salesmen of the upcoming events where they can contact the participents""",

    'description': """
        
    """,

    'author': "Nour Alkbaili",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','event'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/event_views.xml',
        'data/crone.xml',
        'data/mail_template.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}

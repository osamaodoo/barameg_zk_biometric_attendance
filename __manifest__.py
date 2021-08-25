# -*- coding: utf-8 -*-
{
    'name': "barameg_zk_biometric_attendance",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_attendance'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/biometric_devices.xml',
        'views/device_attendance.xml',
        'views/prepared_attendance.xml',
        'views/hr_employee.xml',
        'views/templates.xml',
        'actions/biometric_devices.xml',
        'actions/device_attendance.xml',
        'actions/prepared_attendance.xml',
        'menu/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ]
}

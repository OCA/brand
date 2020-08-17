# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

{
    'name': 'Brand',
    'summary': """
        This is a base addon for brand modules. It adds the brand object and
        its menu and define an abstract model to be inherited from branded
        objects""",
    'version': '12.0.1.1.2',
    'license': 'LGPL-3',
    'author': 'Odoo Community Association (OCA),'
              'ACSONE SA/NV',
    'website': 'https://github.com/OCA/brand',
    'depends': ['base_setup'],
    'data': [
        'views/res_config_settings.xml',
        'security/res_brand.xml',
        'views/res_brand.xml',
    ],
}

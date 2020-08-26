# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Brand External Report Layout',
    'summary': """
        This module allows you to have a different layout by brand for your
        external reports.""",
    'version': '12.0.1.0.2',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/brand',
    'depends': ['base', 'brand', 'web'],
    'data': ['views/res_brand.xml', 'views/report_template.xml'],
}

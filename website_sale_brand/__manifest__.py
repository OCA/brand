# Copyright 2022 Gecko escalade Sàrl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website Sale Brand',
    'summary': """
        Allow setting default brand for website SOs""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Gecko escalade Sàrl,Odoo Community Association (OCA)',
    'depends': [
        'website_sale',
        'sale_brand',
    ],
    'data': [
        'views/res_config_settings.xml',
    ],
    'demo': [
    ],
}

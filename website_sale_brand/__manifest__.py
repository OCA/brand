# Copyright 2026 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Sale Brand",
    "summary": "Configure brands on websites and link them to sales orders",
    "version": "18.0.1.0.0",
    "category": "Website",
    "author": "Onestein, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "license": "AGPL-3",
    "depends": ["website_sale", "sale_brand"],
    "data": [
        "views/website_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}

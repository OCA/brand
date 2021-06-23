# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product brand tags secondary",
    "summary": "Add secondary tags to product brand for a second level of categorization.",
    "version": "14.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Product",
    "depends": [
        "product_brand_tag",
    ],
    "website": "https://github.com/OCA/brand",
    "data": ["views/product_brand_view.xml", "views/product_brand_tag_view.xml"],
    "installable": True,
}

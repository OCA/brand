# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product brand tags",
    "summary": "Add tags to product brand",
    "version": "14.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Product",
    "depends": [
        "product_brand",
    ],
    "website": "https://github.com/OCA/brand",
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/product_brand_view.xml",
        "views/product_brand_tag_view.xml",
    ],
    "installable": True,
}

# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Brand Purchase",
    "summary": """
        This module allows to work with product_brand in purchase reports.""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "depends": ["product_brand", "purchase"],
    "data": ["reports/purchase_report_view.xml", "views/product_brand_view.xml"],
}

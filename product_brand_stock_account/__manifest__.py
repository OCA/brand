# Copyright 2023 Francesco Apruzzese <cescoap@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Brand Stock Account",
    "summary": """
        This module allows to work with product_brand in Stock Account.""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "depends": ["product_brand", "stock_account"],
    "data": ["views/stock_valuation_layer_views.xml"],
}

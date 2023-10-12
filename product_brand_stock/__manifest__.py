# Copyright 2023 Francesco Apruzzese <cescoap@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Brand Stock",
    "summary": """
        This module allows to work with product_brand in Stock.""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "depends": ["product_brand", "stock"],
    "data": [
        "views/stock_quant_views.xml",
        "views/stock_move_views.xml",
        "views/stock_move_line_views.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}

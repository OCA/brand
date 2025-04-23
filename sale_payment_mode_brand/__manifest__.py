# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Payment Mode Brand",
    "summary": """
        This addon limit payment mode selection on sale order to the brand
        allowed payment modes.""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "depends": [
        "sale_brand",
        "account_payment_sale",
        "account_payment_mode_brand",
        "base_view_inheritance_extension",
    ],
    "data": ["views/sale_order.xml"],
}

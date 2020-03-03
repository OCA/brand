# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Payment Mode Brand",
    "summary": """
        This addon define allowed payment mode per brand""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "depends": ["brand", "account_brand", "account_payment_partner"],
    "data": ["views/res_brand.xml", "views/account_invoice.xml"],
}

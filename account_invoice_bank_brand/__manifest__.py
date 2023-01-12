# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Bank Brand",
    "summary": """
        This addon allows to set partner_bank_id on invoices depending on the brand.""",
    "version": "12.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "depends": ["account_brand"],
    "data": ["views/res_brand.xml"],
}

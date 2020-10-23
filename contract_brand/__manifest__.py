# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Contract Brand",
    "summary": """
        This module allows you to manage branded contracts.
        It adds a brand field on the contract and propagate the value on the
        invoices.""",
    "version": "12.0.1.0.3",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/contract",
    "depends": ["contract", "account_brand", "analytic_brand"],
    "data": ["views/contract.xml"],
}

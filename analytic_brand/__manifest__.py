# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Analytic Brand",
    "summary": """
        This addon allows to define analytic distribution models using
        brands in their domains.""",
    "version": "18.0.3.0.1",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "depends": ["analytic", "brand"],
    "data": ["views/account_analytic_distribution_model.xml"],
    "demo": [],
    "maintainers": ["sbejaoui"],
    "external_dependencies": {
        "python": ["openupgradelib"],
    },
}

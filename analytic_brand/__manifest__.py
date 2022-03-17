# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Analytic Brand",
    "summary": """
        This addon associate an analytic account to a brand that will be used
        as a default value where the brand is used if the analytic accounting
        is activated""",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "depends": ["analytic", "brand"],
    "data": ["views/res_brand.xml"],
    "demo": [],
    "maintainers": ["sbejaoui"],
}

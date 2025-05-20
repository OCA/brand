# Copyright 2025 OBS Solutions B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Sale Order Partner Brand Sync",
    "summary": """
        Automatically sets the brand on a Sales Order based on the
        selected customer's brand.
    """,
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Sales",
    "website": "https://github.com/OCA/brand",
    "author": "O.B.S. Solutions, Odoo Community Association (OCA)",
    "maintainers": ["bosd"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "sale_management",
        "sale_brand",
        "partner_brand",
    ],
    "data": [],
}

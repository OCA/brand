# Copyright 2025 OBS Solutions B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Stock Picking Partner Brand Sync",
    "summary": """
        Automatically sets the brand on a Stock Picking based on the
        selected partner's brand.
    """,
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Inventory",
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
        "stock",
        "partner_brand",
        "stock_brand",
    ],
    "data": [],
}

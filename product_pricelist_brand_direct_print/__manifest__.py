# Copyright 2025 OBS Solutions B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Product Pricelist Brand Direct Print",
    "summary": "This module adds brand selection to the "
    "product_pricelist_direct_print wizard."
    "Allowing you to generate branded pricelist PDFs.",
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Sales",
    "website": "https://github.com/OCA/brand",
    "author": "O.B.S. Solutions, Odoo Community Association (OCA)",
    "maintainers": ["bosd"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "preloadable": True,
    "auto_install": False,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "product_pricelist_direct_print",
        "brand",
        "brand_external_report_layout",
    ],
    "data": [
        "wizards/product_pricelist_print_view.xml",
        "reports/report_product_pricelist.xml",
    ],
}

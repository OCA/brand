{
    "name": "Print Product Brand",
    "summary": "This module add the product brand on invoice reports",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/brand",
    "author": "Adhoc SA, Odoo Community Association (OCA)",
    "category": "Warehouse Management",
    "depends": ["product_brand", "sale"],
    "data": ["reports/report_invoice.xml"],
    "installable": True,
    "auto_install": True,
}

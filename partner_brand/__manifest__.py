{
    "name": "Partner Brand",
    "summary": "Define registered mark in partners according to brand settings",
    "version": "16.0.1.0.0",
    "author": "Odoo Community Association (OCA), Akretion",
    "development_status": "Alpha",
    "category": "Product",
    "maintainers": ["bealdav"],
    "website": "https://github.com/OCA/brand",
    "license": "AGPL-3",
    "depends": [
        "brand",
        "contacts",
    ],
    "data": [
        "views/partner.xml",
    ],
    "demo": [
        "data/res_brand_demo.xml",
        "data/res_partner_demo.xml",
    ],
}

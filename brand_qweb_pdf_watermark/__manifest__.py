# Copyright 2026 CIT-Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Brand QWeb PDF Watermark",
    "summary": "Add watermark to Brand reports",
    "version": "18.0.1.0.0",
    "category": "Technical",
    "website": "https://github.com/OCA/brand",
    "author": "CIT-Services, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "brand",
        "report_qweb_pdf_watermark",
    ],
    "data": [
        "views/res_brand_views.xml",
    ],
    "installable": True,
}

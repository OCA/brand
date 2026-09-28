# © 2025 OBS Solutions BV <http://obs-solutions.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Brand Specific PDF watermark",
    "version": "18.0.1.0.0",
    "author": "OBS Solutions BV, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "development_status": "Beta",
    "summary": "Add brand specific watermarks to your QWEB PDF reports",
    "website": "https://github.com/OCA/brand",
    "depends": ["web", "brand_external_report_layout", "report_qweb_pdf_watermark"],
    "data": [
        "views/ir_actions_report_xml.xml",
        "views/res_brand.xml",
    ],
    "assets": {
        "web.report_assets_pdf": [
            "/brand_report_qweb_pdf_watermark/static/src/css/report_qweb_pdf_watermark.css"
        ],
    },
    "installable": True,
}

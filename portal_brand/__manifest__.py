# Copyright 2025 bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Display Brand logo in Portal",
    "summary": """
        Displays the brand logo in the portal.
    """,
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA), bosd",
    "website": "https://github.com/OCA/brand",
    "version": "15.0.1.0.0",
    "depends": ["mail_brand", "brand", "portal"],
    "data": [
        "views/portal_templates.xml",
    ],
}

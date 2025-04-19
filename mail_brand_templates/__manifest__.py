# Copyright 2025 bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Brand Specific Email Templates",
    "summary": """
        Allows to define email templates specific to a brand.
    """,
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA), bosd",
    "website": "https://github.com/OCA/brand",
    "version": "15.0.1.0.0",
    "depends": ["mail_brand", "brand"],
    "data": [
        "wizard/mail_compose_message_view.xml",
        "security/mail_template_security.xml",
        "views/mail_template.xml",
    ],
    "maintainers": ["bosd"],
}

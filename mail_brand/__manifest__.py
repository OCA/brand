# Copyright 2021 Yves Goldberg
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Mail brand",
    "summary": "Adds the concept of brand according mail",
    "version": "13.0.1.0.0",
    "author": "Yves Goldberg (Ygol InternetWork), " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/brand",
    "category": "Mail",
    "depends": ["brand", "mail", "base"],
    "license": "LGPL-3",
    "data": [
        "data/mail_data.xml",
        "security/mail_alias_security.xml",
        "security/mail_template_security.xml",
        "views/brand_views_ext.xml",
        "views/mail_alias_views_ext.xml",
        "views/mail_template_views_ext.xml",
        "wizard/mail_compose_message_view_ext.xml",
    ],
    "installable": True,
}

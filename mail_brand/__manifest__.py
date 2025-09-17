# Copyright 2022 Snakebyte
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Email Brand",
    "summary": """
        If a model has a brand defined to it, emails send from this model will be
        branded accordingly.
    """,
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA), Gert Pellin / Snakebyte Development, bosd",
    "website": "https://github.com/OCA/brand",
    "version": "15.0.1.0.1",
    "depends": ["mail", "brand"],
    "data": [
        "data/mail_template.xml",
        "wizard/mail_compose_message_view.xml",
    ],
    "maintainers": ["switch87", "bosd"],
}

# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import os

from odoo import _, fields, models, tools


class ResBrand(models.Model):

    _inherit = "res.brand"

    def _get_default_brand_logo(self):
        return base64.b64encode(
            open(
                os.path.join(
                    tools.config["root_path"],
                    "addons",
                    "base",
                    "static",
                    "img",
                    "res_company_logo.png",
                ),
                "rb",
            ).read()
        )

    logo = fields.Binary(
        related="partner_id.image_1920",
        default=_get_default_brand_logo,
        string="Brand Logo",
        readonly=False,
    )
    external_report_layout_id = fields.Many2one(
        comodel_name="ir.ui.view", string="Document Template"
    )
    report_header = fields.Text(
        string="Report Header",
        help="Appears by default on the top right corner of your printed "
        "documents (report header).",
    )
    report_footer = fields.Text(
        string="Report Footer",
        translate=True,
        help="Footer text displayed at the bottom of all reports.",
    )
    paperformat_id = fields.Many2one(
        "report.paperformat",
        "Paper format",
        default=lambda self: self.env.ref(
            "base.paperformat_euro", raise_if_not_found=False
        ),
    )

    font = fields.Selection(
        [
            ("Lato", "Lato"),
            ("Roboto", "Roboto"),
            ("Open_Sans", "Open Sans"),
            ("Montserrat", "Montserrat"),
            ("Oswald", "Oswald"),
            ("Raleway", "Raleway"),
        ],
        default="Lato",
    )
    primary_color = fields.Char()
    secondary_color = fields.Char()

    def change_report_template(self):
        self.ensure_one()
        context = {"default_brand_id": self.id}
        context.update(self.env.context)
        return {
            "name": _("Choose Your Document Layout"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "target": "new",
            "res_model": "brand.document.layout",
            "context": context,
        }

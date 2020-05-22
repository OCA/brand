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

    def change_report_template(self):
        self.ensure_one()
        form_view = self.env.ref(
            "brand_external_report_layout.res_brand_document_template_form"
        )
        return {
            "name": _("Choose Your Document Layout"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_id": self.id,
            "res_model": "res.brand",
            "views": [(form_view.id, "form")],
            "view_id": form_view.id,
            "target": "new",
        }

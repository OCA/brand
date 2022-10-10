# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import os

from odoo import _, api, fields, models, tools


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
        help="Appears by default on the top right corner of your printed "
        "documents (report header).",
    )
    report_footer = fields.Text(
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
    company_details = fields.Html(
        string="Brand Details",
        help="Header text displayed at the top of all reports.",
    )
    layout_background = fields.Selection(
        [("Blank", "Blank"), ("Geometric", "Geometric"), ("Custom", "Custom")],
        default="Blank",
        required=True,
    )
    layout_background_image = fields.Binary("Background Image")

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

    def _get_asset_style_b64(self):
        brand_styles = self.env["ir.qweb"]._render(
            "brand_external_report_layout.styles_brand_report",
            {"brand_ids": self.sudo().search([])},
            raise_if_not_found=False,
        )
        return base64.b64encode(brand_styles.encode())

    def _update_asset_style(self):
        asset_attachment = self.env.ref(
            "brand_external_report_layout.asset_styles_brand_report",
            raise_if_not_found=False,
        )
        if not asset_attachment:
            return
        asset_attachment = asset_attachment.sudo()
        b64_val = self._get_asset_style_b64()
        if b64_val != asset_attachment.datas:
            asset_attachment.write({"datas": b64_val})

    @api.model
    def _get_style_fields(self):
        return {"external_report_layout_id", "font", "primary_color", "secondary_color"}

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        style_fields = self._get_style_fields()
        if any(not style_fields.isdisjoint(values) for values in vals_list):
            self._update_asset_style()
        return companies

    def write(self, values):
        res = super().write(values)
        style_fields = self._get_style_fields()
        if not style_fields.isdisjoint(values):
            self._update_asset_style()
        return res

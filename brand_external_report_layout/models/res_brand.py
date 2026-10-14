# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, tools
from odoo.tools import BinaryBytes


class ResBrand(models.Model):
    _inherit = "res.brand"

    def _get_default_brand_logo(self):
        with tools.file_open("base/static/img/res_company_logo.png", "rb") as logo:
            return BinaryBytes(logo.read(), filename="logo.png")

    logo = fields.Binary(
        related="partner_id.image_1920",
        default=lambda self: self._get_default_brand_logo(),
        string="Brand Logo",
        readonly=False,
    )
    external_report_layout_id = fields.Many2one(
        comodel_name="ir.ui.view", string="Document Template"
    )
    report_header = fields.Html(
        help="Appears by default on the top right corner of your printed "
        "documents (report header).",
    )
    report_footer = fields.Html(
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
    report_tables_id = fields.Selection(
        [
            ("light", "Light"),
            ("boxed", "Boxed"),
            ("bold", "Bold"),
            ("striped", "Striped"),
            ("bubble", "Bubble"),
            ("column", "Column"),
            ("compact", "Compact"),
        ],
        string="Table Design",
        default="light",
        required=True,
    )
    font = fields.Selection(
        [
            ("Lato", "Lato"),
            ("Roboto", "Roboto"),
            ("Open_Sans", "Open Sans"),
            ("Montserrat", "Montserrat"),
            ("Oswald", "Oswald"),
            ("Raleway", "Raleway"),
            ("Tajawal", "Tajawal"),
            ("Noto_Sans_Mono", "Noto Sans Mono"),
        ],
        default="Lato",
    )
    primary_color = fields.Char()
    secondary_color = fields.Char()
    company_details = fields.Html(
        string="Brand Details",
        help="Header text displayed at the top of all reports.",
    )
    is_company_details_empty = fields.Boolean(compute="_compute_empty_company_details")

    @api.depends("company_details")
    def _compute_empty_company_details(self):
        for record in self:
            record.is_company_details_empty = not tools.html2plaintext(
                record.company_details or ""
            )

    def change_report_template(self):
        self.ensure_one()
        return {
            "name": self.env._("Configure your document layout"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "target": "new",
            "res_model": "brand.document.layout",
            "context": dict(
                self.env.context, default_brand_id=self.id, dialog_size="extra-large"
            ),
        }

    def _get_asset_style_binary(self):
        brand_styles = self.env["ir.qweb"]._render(
            "brand_external_report_layout.styles_brand_report",
            {
                "brand_ids": self.sudo()
                .with_context(active_test=False)
                .search([], limit=False)
            },
            raise_if_not_found=False,
        )
        return BinaryBytes(brand_styles.encode())

    def _update_asset_style(self):
        asset_attachment = self.env.ref(
            "brand_external_report_layout.asset_styles_brand_report",
            raise_if_not_found=False,
        )
        if not asset_attachment:
            return
        asset_attachment = asset_attachment.sudo()
        styles = self._get_asset_style_binary()
        if styles.content != asset_attachment.raw.content:
            asset_attachment.write({"raw": styles})

    @api.model
    def _get_style_fields(self):
        return {
            "external_report_layout_id",
            "report_tables_id",
            "font",
            "primary_color",
            "secondary_color",
        }

    @api.model_create_multi
    def create(self, vals_list):
        brands = super().create(vals_list)
        self._update_asset_style()
        return brands

    def write(self, values):
        res = super().write(values)
        if not self._get_style_fields().isdisjoint(values):
            self._update_asset_style()
        return res

    def unlink(self):
        res = super().unlink()
        self._update_asset_style()
        return res

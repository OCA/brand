# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import markupsafe

from odoo import api, fields, models

from odoo.addons.web.models.base_document_layout import (
    DEFAULT_PRIMARY,
    DEFAULT_SECONDARY,
)


class BrandDocumentLayout(models.TransientModel):

    _name = "brand.document.layout"
    _description = "Brand Document Layout"
    _inherit = "base.document.layout"

    brand_id = fields.Many2one("res.brand", required=True)

    logo = fields.Binary(related="brand_id.logo", readonly=False)
    report_header = fields.Text(related="brand_id.report_header", readonly=False)
    report_footer = fields.Text(related="brand_id.report_footer", readonly=False)
    paperformat_id = fields.Many2one(related="brand_id.paperformat_id", readonly=False)
    external_report_layout_id = fields.Many2one(
        related="brand_id.external_report_layout_id", readonly=False
    )

    font = fields.Selection(related="brand_id.font", readonly=False)
    primary_color = fields.Char(related="brand_id.primary_color", readonly=False)
    secondary_color = fields.Char(related="brand_id.secondary_color", readonly=False)
    company_details = fields.Html(related="brand_id.company_details", readonly=False)
    layout_background = fields.Selection(
        related="brand_id.layout_background", readonly=False
    )
    layout_background_image = fields.Binary(
        related="brand_id.layout_background_image", readonly=False
    )

    @api.onchange("company_id")
    def _onchange_company_id(self):
        return {}

    @api.onchange("brand_id")
    def _onchange_brand_id(self):
        for wizard in self:
            wizard.logo = wizard.brand_id.logo
            wizard.report_header = wizard.brand_id.report_header
            wizard.report_footer = (
                wizard.brand_id.report_footer
                if isinstance(wizard.brand_id.report_footer, str)
                else wizard.report_footer
            )
            wizard.company_details = (
                wizard.brand_id.company_details
                if isinstance(wizard.brand_id.company_details, str)
                else wizard.company_details
            )
            wizard.paperformat_id = wizard.brand_id.paperformat_id
            wizard.external_report_layout_id = wizard.brand_id.external_report_layout_id
            wizard.font = wizard.brand_id.font
            wizard.primary_color = wizard.brand_id.primary_color
            wizard.secondary_color = wizard.brand_id.secondary_color
            wizard_layout = wizard.env["report.layout"].search(
                [("view_id.key", "=", wizard.brand_id.external_report_layout_id.key)]
            )
            wizard.report_layout_id = wizard_layout or wizard_layout.search([], limit=1)

            if not wizard.primary_color:
                wizard.primary_color = wizard.logo_primary_color or DEFAULT_PRIMARY
            if not wizard.secondary_color:
                wizard.secondary_color = (
                    wizard.logo_secondary_color or DEFAULT_SECONDARY
                )

    @api.onchange("logo")
    def _onchange_logo(self):
        for wizard in self:
            brand = wizard.brand_id
            if (
                wizard.logo == brand.logo
                and brand.primary_color
                and brand.secondary_color
            ):
                continue

            if wizard.logo_primary_color:
                wizard.primary_color = wizard.logo_primary_color
            if wizard.logo_secondary_color:
                wizard.secondary_color = wizard.logo_secondary_color

    def _get_asset_style(self):
        return self.env["ir.qweb"]._render(
            "brand_external_report_layout.styles_brand_report",
            {"brand_ids": self},
            raise_if_not_found=False,
        )

    @api.depends(
        "report_layout_id",
        "logo",
        "font",
        "primary_color",
        "secondary_color",
        "report_header",
        "report_footer",
        "layout_background",
        "layout_background_image",
        "company_details",
    )
    def _compute_preview(self):
        styles = self._get_asset_style()
        for wizard in self:
            if wizard.report_layout_id:
                if wizard.env.context.get("bin_size"):
                    wizard_with_logo = wizard.with_context(bin_size=False)
                else:
                    wizard_with_logo = wizard
                preview_css = markupsafe.Markup(
                    self._get_css_for_preview(styles, wizard_with_logo.id)
                )
                ir_ui_view = wizard_with_logo.env["ir.ui.view"]
                wizard.preview = ir_ui_view._render_template(
                    "web.report_invoice_wizard_preview",
                    {
                        "brand": wizard_with_logo,
                        "company": wizard_with_logo,
                        "preview_css": preview_css,
                    },
                )
            else:
                wizard.preview = False

# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from markupsafe import Markup

from odoo import api, fields, models

from odoo.addons.base.models.ir_qweb_fields import nl2br_enclose
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
    report_header = fields.Html(related="brand_id.report_header", readonly=False)
    report_footer = fields.Html(
        related="brand_id.report_footer", readonly=False, default=None
    )
    paperformat_id = fields.Many2one(related="brand_id.paperformat_id", readonly=False)
    external_report_layout_id = fields.Many2one(
        related="brand_id.external_report_layout_id", readonly=False
    )
    report_tables_id = fields.Selection(
        related="brand_id.report_tables_id", readonly=False
    )
    font = fields.Selection(related="brand_id.font", readonly=False)
    primary_color = fields.Char(related="brand_id.primary_color", readonly=False)
    secondary_color = fields.Char(related="brand_id.secondary_color", readonly=False)
    company_details = fields.Html(
        related="brand_id.company_details", readonly=False, default=None
    )

    partner_id = fields.Many2one(related="brand_id.partner_id", readonly=True)
    phone = fields.Char(related="brand_id.phone", readonly=True)
    email = fields.Char(related="brand_id.email", readonly=True)
    website = fields.Char(related="brand_id.website", readonly=True)
    vat = fields.Char(related="brand_id.vat", readonly=True)
    name = fields.Char(related="brand_id.name", readonly=True)
    country_id = fields.Many2one(related="brand_id.country_id", readonly=True)

    @api.onchange("company_id")
    def _onchange_company_id(self):
        return {}

    @api.onchange("brand_id")
    def _onchange_brand_id(self):
        for wizard in self:
            brand = wizard.brand_id
            wizard.logo = brand.logo
            wizard.report_header = brand.report_header
            wizard.report_footer = (
                brand.report_footer
                if isinstance(brand.report_footer, str)
                else Markup(" ").join(
                    value
                    for value in (brand.phone, brand.email, brand.website, brand.vat)
                    if value
                )
            )
            wizard.company_details = (
                brand.company_details
                if isinstance(brand.company_details, str)
                else nl2br_enclose(brand.partner_id.contact_address or "", "div")
            )
            wizard.paperformat_id = brand.paperformat_id
            wizard.external_report_layout_id = brand.external_report_layout_id
            wizard.report_tables_id = brand.report_tables_id
            wizard.font = brand.font
            wizard.primary_color = brand.primary_color
            wizard.secondary_color = brand.secondary_color
            wizard_layout = wizard.env["report.layout"].search(
                [("view_id", "=", brand.external_report_layout_id.id)], limit=1
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
                wizard.logo.content == brand.logo.content
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

    def _get_render_information(self, styles):
        return dict(super()._get_render_information(styles), brand=self)

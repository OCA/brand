# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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

    @api.onchange("company_id")
    def _onchange_company_id(self):
        return {}

    @api.onchange("brand_id")
    def _onchange_brand_id(self):
        for wizard in self:
            wizard.logo = wizard.brand_id.logo
            wizard.report_header = wizard.brand_id.report_header
            wizard.report_footer = wizard.brand_id.report_footer
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

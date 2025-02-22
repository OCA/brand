# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import os
from unittest.mock import patch

import markupsafe

from odoo.tests.common import TransactionCase, tagged

DEFAULT_PRIMARY = "#00ADEF"
DEFAULT_SECONDARY = "#123456"


@tagged("post_install", "-at_install")
class TestBrandExternalReportLayout(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand = cls.env["res.brand"].create({"name": "brand"})
        cls.external_layout_view = cls.env.ref("web.external_layout_standard")
        cls.report_layout = cls.env["report.layout"].create(
            {
                "name": "Test Layout",
                "view_id": cls.external_layout_view.id,
            }  # Access the id
        )
        cls.paperformat = cls.env["report.paperformat"].create(
            {"name": "Test Paperformat"}
        )

    def test_get_default_brand_logo(self):
        self.assertEqual(self.brand.logo, self.brand._get_default_brand_logo())

    def test_brand_document_layout_onchange_brand_id(self):
        wizard = self.env["brand.document.layout"].create({"brand_id": self.brand.id})

        self.assertEqual(wizard.logo, self.brand.logo)
        self.assertEqual(wizard.report_header, self.brand.report_header)
        self.assertEqual(wizard.report_footer, self.brand.report_footer)
        self.assertEqual(wizard.company_details, self.brand.company_details)
        self.assertEqual(wizard.paperformat_id, self.brand.paperformat_id)
        self.assertEqual(
            wizard.external_report_layout_id, self.brand.external_report_layout_id
        )
        self.assertEqual(wizard.font, self.brand.font)
        self.assertEqual(wizard.primary_color, self.brand.primary_color)
        self.assertEqual(wizard.secondary_color, self.brand.secondary_color)
        self.assertEqual(
            wizard.report_layout_id.view_id, self.brand.external_report_layout_id
        )

        self.brand.primary_color = False
        self.brand.secondary_color = False
        self.env.invalidate_all()
        wizard._onchange_brand_id()
        # Get the expected colors from the logo
        expected_primary, expected_secondary = (
            wizard.extract_image_primary_secondary_colors(wizard.logo)
        )
        self.assertEqual(wizard.primary_color, expected_primary)
        self.assertEqual(wizard.secondary_color, expected_secondary)

        module_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(
            module_path, "..", "static", "description", "icon.png"
        )
        with open(image_path, "rb") as image_file:
            base64.b64encode(image_file.read())

        self.brand.primary_color = False
        self.brand.secondary_color = False
        self.env["res.brand"].invalidate_recordset()
        wizard._onchange_brand_id()

        # Extract colors from the logo
        expected_primary, expected_secondary = (
            wizard.extract_image_primary_secondary_colors(wizard.logo)
        )

        self.assertEqual(wizard.primary_color, expected_primary)
        self.assertEqual(wizard.secondary_color, expected_secondary)

    def test_brand_document_layout_onchange_logo(self):
        wizard = self.env["brand.document.layout"].create({"brand_id": self.brand.id})

        module_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(
            module_path, "..", "static", "description", "icon.png"
        )
        with open(image_path, "rb") as image_file:
            logo_data = base64.b64encode(image_file.read())

        wizard.logo = logo_data
        wizard.logo_primary_color = "#AAAAAA"
        wizard.logo_secondary_color = "#BBBBBB"
        wizard._onchange_logo()
        self.assertEqual(wizard.primary_color, "#AAAAAA")
        self.assertEqual(wizard.secondary_color, "#BBBBBB")

        self.brand.primary_color = "#111111"
        self.brand.secondary_color = "#222222"
        wizard.logo = self.brand.logo
        wizard._onchange_logo()
        self.assertEqual(wizard.primary_color, "#AAAAAA")
        self.assertEqual(wizard.secondary_color, "#BBBBBB")

        self.brand.primary_color = "#111111"
        self.brand.secondary_color = "#222222"
        wizard.logo = self.brand.logo
        self.brand.logo = logo_data
        wizard.logo = logo_data
        wizard.logo_primary_color = False
        wizard.logo_secondary_color = False
        wizard._onchange_logo()

        self.brand.primary_color = (
            False  # Temporarily set brand's primary_color to False
        )
        self.brand.secondary_color = False
        wizard.logo = False
        self.assertFalse(wizard.primary_color)
        self.assertFalse(wizard.secondary_color)

    def test_brand_document_layout_compute_preview(self):
        wizard = self.env["brand.document.layout"].create(
            {
                "brand_id": self.brand.id,
                "report_layout_id": self.report_layout.id,
                "paperformat_id": self.paperformat.id,
            }
        )

        with (
            patch.object(
                type(wizard), "_get_css_for_preview", return_value="test_css"
            ) as mock_css,
            patch.object(
                type(wizard.env["ir.ui.view"]),
                "_render_template",
                return_value="test_html",
            ) as mock_render,
        ):
            wizard._compute_preview()
            self.assertTrue(wizard.preview)
            mock_css.assert_called_once()
            mock_render.assert_called_once()
            self.assertEqual(
                mock_render.call_args[0][0], "web.report_invoice_wizard_preview"
            )

        wizard.report_layout_id = False
        wizard._compute_preview()
        self.assertFalse(wizard.preview)

    def test_brand_document_layout_compute_preview_bin_size(self):
        wizard = self.env["brand.document.layout"].create(
            {
                "brand_id": self.brand.id,
                "report_layout_id": self.report_layout.id,
                "paperformat_id": self.paperformat.id,
            }
        )
        with (
            patch.object(type(wizard), "_get_css_for_preview", return_value="test_css"),
            patch.object(
                type(wizard.env["ir.ui.view"]),
                "_render_template",
                return_value="test_html",
            ) as mock_render,
        ):
            wizard_with_bin_size = wizard.with_context(bin_size=True)
            wizard_with_bin_size._compute_preview()
            mock_render.assert_called_once()
            self.assertEqual(
                mock_render.call_args[0][0], "web.report_invoice_wizard_preview"
            )

    def test_brand_document_layout_get_asset_style(self):
        wizard = self.env["brand.document.layout"].create(
            {
                "brand_id": self.brand.id,
                "report_layout_id": self.report_layout.id,
                "paperformat_id": self.paperformat.id,
            }
        )
        result = wizard._get_asset_style()
        self.assertIsInstance(result, markupsafe.Markup)

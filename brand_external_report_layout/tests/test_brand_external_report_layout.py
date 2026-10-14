# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import html

from odoo.tests import Form, TransactionCase, tagged
from odoo.tools import BinaryValue


@tagged("post_install", "-at_install")
class TestBrandExternalReportLayout(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand = cls.env["res.brand"].create(
            {
                "name": "Report Brand",
                "email": "brand@example.com",
                "phone": "+1 809 555 0100",
                "street": "Brand Street",
                "country_id": cls.env.ref("base.do").id,
                "primary_color": "#123456",
                "secondary_color": "#654321",
            }
        )
        cls.layouts = cls.env["report.layout"].search([])
        cls.standard_layout = cls.layouts.filtered(
            lambda layout: layout.view_id == cls.env.ref("web.external_layout_standard")
        )[:1]

    def _new_wizard(self):
        return self.env["brand.document.layout"].create(
            {
                "brand_id": self.brand.id,
                "report_layout_id": self.standard_layout.id,
            }
        )

    def test_default_logo(self):
        self.assertIsInstance(self.brand.logo, BinaryValue)
        self.assertTrue(self.brand.logo.content)
        wizard = self._new_wizard()
        self.assertTrue(all(wizard.extract_image_primary_secondary_colors(wizard.logo)))

    def test_wizard_uses_brand_details(self):
        self.env.company.write(
            {
                "report_footer": "Company-only footer",
                "company_details": "Company-only address",
            }
        )
        wizard = self._new_wizard()
        self.assertFalse(wizard.report_footer)
        self.assertFalse(wizard.company_details)
        wizard._onchange_brand_id()
        self.assertEqual(wizard.partner_id, self.brand.partner_id)
        self.assertEqual(wizard.country_id, self.brand.country_id)
        self.assertEqual(wizard.name, self.brand.name)
        self.assertIn("brand@example.com", wizard.report_footer)
        self.assertIn("Brand Street", wizard.company_details)
        self.assertNotIn("Company-only", wizard.report_footer)
        self.assertNotIn("Company-only", wizard.company_details)

    def test_wizard_saves_brand_table_style(self):
        company_style = self.env.company.report_tables_id
        with Form(
            self.env["brand.document.layout"].with_context(
                default_brand_id=self.brand.id
            )
        ) as wizard:
            wizard.report_tables_id = "striped"
            wizard.font = "Noto_Sans_Mono"
        self.assertEqual(self.brand.report_tables_id, "striped")
        self.assertEqual(self.brand.font, "Noto_Sans_Mono")
        self.assertEqual(self.env.company.report_tables_id, company_style)

    def test_brand_colors_preserved_for_original_logo(self):
        wizard = self._new_wizard()
        wizard._onchange_logo()
        self.assertEqual(wizard.primary_color, "#123456")
        self.assertEqual(wizard.secondary_color, "#654321")

    def test_default_colors_without_logo(self):
        self.brand.write(
            {"logo": False, "primary_color": False, "secondary_color": False}
        )
        wizard = self._new_wizard()
        wizard._onchange_brand_id()
        self.assertEqual(wizard.primary_color, "#000000")
        self.assertEqual(wizard.secondary_color, "#000000")

    def test_preview_all_layouts(self):
        wizard = self._new_wizard()
        for layout in self.layouts:
            with self.subTest(layout=layout.view_id.key):
                wizard.report_layout_id = layout
                wizard._onchange_report_layout_id()
                preview = html.fromstring(wizard.preview)
                for section in ("header", "article", "footer"):
                    sections = preview.xpath(
                        f"//div[contains(concat(' ', normalize-space(@class), ' '),"
                        f" ' {section} ')]"
                    )
                    self.assertEqual(len(sections), 1)
                    self.assertIn(
                        f"o_brand_{wizard.id}_layout", sections[0].get("class")
                    )
                self.assertIn(self.brand.name, preview.text_content())
                self.assertIn("#123456", wizard.preview)

    def test_preview_all_table_styles(self):
        wizard = self._new_wizard()
        wizard._onchange_report_layout_id()
        table_classes = {
            "light": "o_table_standard",
            "boxed": "o_table_boxed",
            "bold": "o_table_bold",
            "striped": "o_table_striped",
            "bubble": "o_table_boxed-rounded",
            "column": "o_table_column",
            "compact": "o_table_compact",
        }
        for table_style, table_class in table_classes.items():
            with self.subTest(table_style=table_style):
                wizard.report_tables_id = table_style
                self.assertIn(table_class, wizard.preview)
                self.assertIn(f".o_brand_{wizard.id}_layout", wizard.preview)
        wizard.report_layout_id = False
        self.assertFalse(wizard.preview)

    def test_company_report_without_brand(self):
        wizard = self.env["base.document.layout"].create(
            {"report_layout_id": self.standard_layout.id}
        )
        wizard._onchange_report_layout_id()
        self.assertIn(f"o_company_{wizard.id}_layout", wizard.preview)
        self.assertNotIn("o_brand_", wizard.preview)

    def test_report_uses_brand_layout(self):
        self.brand.external_report_layout_id = self.standard_layout.view_id
        report = self.env["ir.qweb"]._render(
            "web.external_layout",
            {
                "brand": self.brand,
                "o": self.brand.partner_id,
                "res_company": self.env.company,
                "report_type": "html",
            },
        )
        self.assertIn(f"o_brand_{self.brand.id}_layout", report)
        self.assertIn(self.brand.name, report)
        self.assertNotIn(f"o_company_{self.brand.id}_layout", report)

    def test_report_selects_document_brand(self):
        self.brand.external_report_layout_id = self.standard_layout.view_id
        document = self._new_wizard()
        report = self.env["ir.qweb"]._render(
            "web.external_layout",
            {
                "o": document,
                "res_company": self.env.company,
                "report_type": "html",
            },
        )
        self.assertIn(f"o_brand_{self.brand.id}_layout", report)
        self.assertIn(self.brand.name, report)

    def test_report_falls_back_to_company_layout(self):
        document = self._new_wizard()
        report = self.env["ir.qweb"]._render(
            "web.external_layout",
            {
                "o": document,
                "res_company": self.env.company,
                "report_type": "html",
            },
        )
        self.assertIn(f"o_company_{self.env.company.id}_layout", report)
        self.assertNotIn("o_brand_", report)

    def test_asset_updates_for_default_brand_and_table_style(self):
        attachment = self.env.ref(
            "brand_external_report_layout.asset_styles_brand_report"
        )
        brand = self.env["res.brand"].create({"name": "Default Brand"})
        selector = f".o_brand_{brand.id}_layout"
        self.assertIn(selector, attachment.raw.decode())
        old_styles = attachment.raw.content
        brand.report_tables_id = "boxed"
        self.assertNotEqual(old_styles, attachment.raw.content)
        self.assertIn("o_report_layout_boxed", attachment.raw.decode())
        brand.unlink()
        self.assertNotIn(selector, attachment.raw.decode())

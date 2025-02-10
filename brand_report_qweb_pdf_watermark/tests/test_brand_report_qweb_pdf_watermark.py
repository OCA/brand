# © 2025 OBS Solutions BV <http://obs-solutions.com>
import base64
import os

from odoo_test_helper import FakeModelLoader

from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestBrandReportWatermark(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context))
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()

        from .test_brand_report_qweb_pdf_watermakr_tester import (
            BrandReportQwebPdfWatermarkTester,
        )

        cls.loader.update_registry((BrandReportQwebPdfWatermarkTester,))
        cls.test_model = cls.env[BrandReportQwebPdfWatermarkTester._name]
        cls.tester_model = cls.env["ir.model"].search(
            [("model", "=", "brand.report.qweb.pdf.watermark.tester")]
        )

        cls.report_model = cls.env["ir.actions.report"]
        cls.brand_model = cls.env["res.brand"]

        # Load PDF watermark from static/images folder
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(module_path, "examples/Watermark_example_1.pdf")

        with open(image_path, "rb") as f:
            watermark_content = f.read()

        # Create a brand with a watermark
        cls.brand = cls.brand_model.with_context(create_res_partner=False).create(
            {
                "name": "Test Brand",
                "pdf_watermark": base64.b64encode(watermark_content).decode("ascii"),
            }
        )

        # Find or create a report action for the temporary model
        cls.report_action = cls.env["ir.actions.report"].search(
            [("model", "=", "brand.report.qweb.pdf.watermark.tester")], limit=1
        )
        if not cls.report_action:
            cls.report_action = cls.env["ir.actions.report"].create(
                {
                    "name": "test_report",
                    "report_name": "test_report",
                    "model": "brand.report.qweb.pdf.watermark.tester",
                    "report_type": "qweb-pdf",
                    "use_brand_watermark": True,
                }
            )

    def tearDown(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    def test_postprocess_wkhtmltopdf_with_watermark(self):
        record = self.test_model.create({"brand_id": self.brand.id})
        self.env.context = {
            "res_ids": [record.id],
            "active_model": self.test_model._name,
        }

        self.report_action.report_name = "test_report"

        # Load PDF watermark
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(module_path, "examples/Watermark_example_2.pdf")
        with open(image_path, "rb") as f:
            watermark_content = f.read()
        sample_pdf_data = watermark_content

        result = self.report_action._postprocess_wkhtmltopdf(
            sample_pdf_data, report_ref=self.report_action.report_name
        )

        self.assertTrue(result)
        self.assertNotEqual(
            result, sample_pdf_data
        )  # Check if the PDF content has changed

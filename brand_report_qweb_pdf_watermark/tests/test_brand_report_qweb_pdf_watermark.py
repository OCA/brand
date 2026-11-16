# © 2025 OBS Solutions BV <http://obs-solutions.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
from unittest.mock import patch

from odoo_test_helper import FakeModelLoader

from odoo.tests import common, tagged
from odoo.tools.misc import file_open

from odoo.addons.base.models.ir_actions_report import IrActionsReport


def _read_example(name):
    with file_open(f"brand_report_qweb_pdf_watermark/examples/{name}", "rb") as f:
        return f.read()


@tagged("post_install", "-at_install")
class TestBrandReportWatermark(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()

        from .test_brand_report_qweb_pdf_watermark_tester import (
            BrandReportQwebPdfWatermarkTester,
        )

        cls.loader.update_registry((BrandReportQwebPdfWatermarkTester,))
        cls.test_model = cls.env[BrandReportQwebPdfWatermarkTester._name]

        cls.watermark_1 = _read_example("Watermark_example_1.pdf")
        cls.watermark_2 = _read_example("Watermark_example_2.pdf")
        cls.brand = (
            cls.env["res.brand"]
            .with_context(create_res_partner=False)
            .create(
                {
                    "name": "Test Brand",
                    "pdf_watermark": base64.b64encode(cls.watermark_1),
                }
            )
        )
        cls.record = cls.test_model.create({"brand_id": cls.brand.id})
        cls.report_action = cls.env["ir.actions.report"].create(
            {
                "name": "test_report",
                "report_name": "test_report",
                "model": cls.test_model._name,
                "report_type": "qweb-pdf",
                "use_brand_watermark": True,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    def _run(self, record):
        """Run the watermark chain with wkhtmltopdf replaced by a sample pdf."""
        sample_pdf = self.watermark_2
        with patch.object(
            IrActionsReport,
            "_run_wkhtmltopdf",
            lambda self, bodies, **kwargs: sample_pdf,
        ):
            return (
                self.env["ir.actions.report"]
                .with_context(res_ids=record.ids)
                ._run_wkhtmltopdf([], report_ref=self.report_action.report_name)
            )

    def test_brand_watermark_applied(self):
        result = self._run(self.record)
        self.assertTrue(result.startswith(b"%PDF"))
        self.assertNotEqual(result, self.watermark_2)

    def test_no_brand_watermark_when_disabled(self):
        self.report_action.use_brand_watermark = False
        self.assertEqual(self._run(self.record), self.watermark_2)

    def test_no_brand_watermark_without_brand(self):
        record = self.test_model.create({})
        self.assertEqual(self._run(record), self.watermark_2)

    def test_stack_company_and_brand_watermark(self):
        self.env.company.pdf_watermark = base64.b64encode(self.watermark_1)
        self.report_action.write(
            {"use_company_watermark": True, "use_brand_watermark": False}
        )
        company_only = self._run(self.record)
        self.assertNotEqual(company_only, self.watermark_2)

        self.report_action.use_brand_watermark = True
        stacked = self._run(self.record)
        self.assertNotEqual(stacked, company_only)
        self.assertGreater(len(stacked), len(company_only))

    def test_invalid_brand_watermark(self):
        self.brand.pdf_watermark = base64.b64encode(b"not a pdf nor an image")
        with self.assertLogs(
            "odoo.addons.brand_report_qweb_pdf_watermark.models.report", "ERROR"
        ):
            self.assertEqual(self._run(self.record), self.watermark_2)

    def test_image_brand_watermark(self):
        with file_open(
            "brand_report_qweb_pdf_watermark/static/description/icon.png", "rb"
        ) as f:
            self.brand.pdf_watermark = base64.b64encode(f.read())
        result = self._run(self.record)
        self.assertTrue(result.startswith(b"%PDF"))
        self.assertNotEqual(result, self.watermark_2)

# Copyright 2026 CIT-Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from unittest.mock import MagicMock, patch

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestBrandQwebPdfWatermark(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        patcher = patch.dict(
            type(cls.env["res.company"])._fields, {"brand_id": MagicMock()}
        )
        patcher.start()
        cls.addClassCleanup(patcher.stop)

        cls.raw_watermark_1 = b"%PDF-1.4 Mock Watermark 1 Content"
        cls.raw_watermark_2 = b"%PDF-1.4 Mock Watermark 2 Content"
        cls.b64_watermark_1 = base64.b64encode(cls.raw_watermark_1)
        cls.b64_watermark_2 = base64.b64encode(cls.raw_watermark_2)

        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.brand_with_watermark = cls.env["res.brand"].create(
            {
                "name": "Brand Watermark 1",
                "pdf_watermark": cls.b64_watermark_1,
            }
        )
        cls.brand_with_watermark_2 = cls.env["res.brand"].create(
            {
                "name": "Brand Watermark 2",
                "pdf_watermark": cls.b64_watermark_2,
            }
        )
        cls.brand_no_watermark = cls.env["res.brand"].create(
            {
                "name": "Brand No Watermark",
            }
        )
        cls.report = cls.env["ir.actions.report"].create(
            {
                "name": "Test Action Report",
                "model": "res.company",
                "report_name": "test_action_report",
            }
        )

    def _create_mock_docs(self, doc_list):
        mock_docs = MagicMock()
        mock_docs.__iter__.return_value = doc_list
        mock_docs.__getitem__.side_effect = doc_list.__getitem__
        mock_docs.__bool__.return_value = bool(doc_list)
        mock_docs.__len__.return_value = len(doc_list)
        brands = self.env["res.brand"]
        for d in doc_list:
            brand_id = getattr(d, "brand_id", False)
            if brand_id:
                brands |= brand_id
        mock_docs.mapped.return_value = brands
        return mock_docs

    def test_watermark_field_on_brand(self):
        """Test that pdf_watermark is correctly stored and retrieved on res.brand."""
        self.assertEqual(self.brand_with_watermark.pdf_watermark, self.b64_watermark_1)
        self.assertFalse(self.brand_no_watermark.pdf_watermark)

    def test_get_watermark_no_docids(self):
        """When docids is False or empty, fallback cleanly to None."""
        watermark = self.env["ir.actions.report"]._get_watermark(
            self.report, docids=False
        )
        self.assertIsNone(watermark)

    def test_get_watermark_model_without_brand_id(self):
        """When model has no brand_id in _fields, fallback cleanly to None."""
        report_no_brand = self.env["ir.actions.report"].create(
            {
                "name": "Report Without Brand Model",
                "model": "res.users",
                "report_name": "test_report_without_brand_model",
            }
        )
        watermark = self.env["ir.actions.report"]._get_watermark(
            report_no_brand, docids=[self.env.user.id]
        )
        self.assertIsNone(watermark)

    def test_get_watermark_single_brand_with_watermark(self):
        """When documents belong to a single brand, return decoded watermark."""
        mock_doc = MagicMock()
        mock_doc.brand_id = self.brand_with_watermark
        mock_docs = self._create_mock_docs([mock_doc])

        with patch.object(
            type(self.env["res.company"]), "browse", return_value=mock_docs
        ):
            watermark = self.env["ir.actions.report"]._get_watermark(
                self.report, docids=[1]
            )
            self.assertEqual(watermark, self.raw_watermark_1)

    def test_get_watermark_multiple_docs_same_brand(self):
        """When multiple docs belong to the same brand, return decoded watermark."""
        mock_doc1 = MagicMock()
        mock_doc1.brand_id = self.brand_with_watermark
        mock_doc2 = MagicMock()
        mock_doc2.brand_id = self.brand_with_watermark
        mock_docs = self._create_mock_docs([mock_doc1, mock_doc2])

        with patch.object(
            type(self.env["res.company"]), "browse", return_value=mock_docs
        ):
            watermark = self.env["ir.actions.report"]._get_watermark(
                self.report, docids=[1, 2]
            )
            self.assertEqual(watermark, self.raw_watermark_1)

    def test_get_watermark_single_brand_without_watermark(self):
        """When document brand has no watermark, fallback cleanly to None."""
        mock_doc = MagicMock()
        mock_doc.brand_id = self.brand_no_watermark
        mock_docs = self._create_mock_docs([mock_doc])

        with patch.object(
            type(self.env["res.company"]), "browse", return_value=mock_docs
        ):
            watermark = self.env["ir.actions.report"]._get_watermark(
                self.report, docids=[1]
            )
            self.assertIsNone(watermark)

    def test_get_watermark_doc_without_brand(self):
        """When document has False brand_id, fallback cleanly to None."""
        mock_doc = MagicMock()
        mock_doc.brand_id = False
        mock_docs = self._create_mock_docs([mock_doc])

        with patch.object(
            type(self.env["res.company"]), "browse", return_value=mock_docs
        ):
            watermark = self.env["ir.actions.report"]._get_watermark(
                self.report, docids=[1]
            )
            self.assertIsNone(watermark)

    def test_get_watermark_multiple_brands_raises_user_error(self):
        """When documents belong to different brands, raise UserError."""
        mock_doc1 = MagicMock()
        mock_doc1.brand_id = self.brand_with_watermark
        mock_doc2 = MagicMock()
        mock_doc2.brand_id = self.brand_with_watermark_2
        mock_docs = self._create_mock_docs([mock_doc1, mock_doc2])

        with patch.object(
            type(self.env["res.company"]), "browse", return_value=mock_docs
        ):
            with self.assertRaises(UserError) as cm:
                self.env["ir.actions.report"]._get_watermark(self.report, docids=[1, 2])
            self.assertIn(
                "Cannot print documents belonging to different brands",
                str(cm.exception),
            )

    def test_get_watermark_mixed_brand_and_no_brand_raises_user_error(self):
        """When documents have a brand and another has no brand, raise UserError."""
        mock_doc1 = MagicMock()
        mock_doc1.brand_id = self.brand_with_watermark
        mock_doc2 = MagicMock()
        mock_doc2.brand_id = False
        mock_docs = self._create_mock_docs([mock_doc1, mock_doc2])

        with patch.object(
            type(self.env["res.company"]), "browse", return_value=mock_docs
        ):
            with self.assertRaises(UserError) as cm:
                self.env["ir.actions.report"]._get_watermark(self.report, docids=[1, 2])
            self.assertIn(
                "Some of the documents do not have a brand", str(cm.exception)
            )

    def test_get_watermark_brand_takes_precedence_over_report_watermark(self):
        """When report has its own watermark, brand watermark takes precedence."""
        report_with_watermark = self.env["ir.actions.report"].create(
            {
                "name": "Report With Own Watermark",
                "model": "res.company",
                "report_name": "report_with_own_watermark",
                "pdf_watermark": self.b64_watermark_2,
            }
        )
        mock_doc = MagicMock()
        mock_doc.brand_id = self.brand_with_watermark
        mock_docs = self._create_mock_docs([mock_doc])

        with patch.object(
            type(self.env["res.company"]), "browse", return_value=mock_docs
        ):
            watermark = self.env["ir.actions.report"]._get_watermark(
                report_with_watermark, docids=[1]
            )
            self.assertEqual(watermark, self.raw_watermark_1)

    def test_get_watermark_fallback_to_report_watermark(self):
        """When doc brand has no watermark, fallback to report's own watermark."""
        report_with_watermark = self.env["ir.actions.report"].create(
            {
                "name": "Report With Own Watermark 2",
                "model": "res.company",
                "report_name": "report_with_own_watermark_2",
                "pdf_watermark": self.b64_watermark_2,
            }
        )
        mock_doc = MagicMock()
        mock_doc.brand_id = self.brand_no_watermark
        mock_docs = self._create_mock_docs([mock_doc])

        with patch.object(
            type(self.env["res.company"]), "browse", return_value=mock_docs
        ):
            watermark = self.env["ir.actions.report"]._get_watermark(
                report_with_watermark, docids=[1]
            )
            self.assertEqual(watermark, self.raw_watermark_2)

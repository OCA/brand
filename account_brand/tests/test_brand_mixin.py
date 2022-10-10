# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.exceptions import ValidationError
from odoo.tests.common import Form, TransactionCase

from odoo.addons.brand.models.res_company import BRAND_USE_LEVEL_REQUIRED_LEVEL


class TestBrandMixin(TransactionCase):
    def setUp(self):
        super(TestBrandMixin, self).setUp()
        self.partner = self.env.user.partner_id
        self.company = self.env.user.company_id
        self.other_company = self.env["res.company"].create(
            {"name": "other company", "parent_id": self.company.id}
        )
        self.journal = self.env["account.journal"].create(
            {"type": "sale", "code": "SALE", "name": "Sale journal"}
        )
        self.invoice = self.env["account.move"].create(
            {
                "name": "Sample invoice",
                "company_id": self.company.id,
                "journal_id": self.journal.id,
                "partner_id": self.partner.id,
            }
        )
        self.brand = self.env["res.brand"].create({"name": "brand"})
        self.other_company_brand = self.env["res.brand"].create(
            {"name": "brand", "company_id": self.other_company.id}
        )

    def test_is_brand_required(self):
        self.assertFalse(self.invoice._is_brand_required())
        self.company.brand_use_level = BRAND_USE_LEVEL_REQUIRED_LEVEL
        self.assertTrue(self.invoice._is_brand_required())

    def test_check_brand_requirement(self):
        self.env["account.move"].create(
            {
                "name": "Sample invoice",
                "company_id": self.company.id,
                "journal_id": self.journal.id,
                "partner_id": self.partner.id,
            }
        )
        self.company.brand_use_level = BRAND_USE_LEVEL_REQUIRED_LEVEL
        with self.assertRaises(ValidationError):
            self.env["account.move"].create(
                {
                    "name": "Sample invoice",
                    "company_id": self.company.id,
                    "journal_id": self.journal.id,
                    "partner_id": self.partner.id,
                }
            )
        self.env["account.move"].create(
            {
                "name": "Sample invoice",
                "company_id": self.company.id,
                "journal_id": self.journal.id,
                "partner_id": self.partner.id,
                "brand_id": self.brand.id,
            }
        )

    def test_check_brand_company_id(self):
        invoice = self.env["account.move"].create(
            {
                "name": "Sample invoice",
                "company_id": self.company.id,
                "journal_id": self.journal.id,
                "partner_id": self.partner.id,
                "brand_id": self.brand.id,
            }
        )
        with self.assertRaises(ValidationError):
            invoice.brand_id = self.other_company_brand

    def test_onchange_brand_id(self):
        new_invoice = self.env["account.move"].new(
            {
                "name": "Sample invoice",
                "company_id": self.company.id,
                "journal_id": self.journal.id,
                "partner_id": self.partner.id,
                "brand_id": self.brand.id,
            }
        )
        self.assertEqual(new_invoice.company_id, self.company)
        new_invoice.brand_id = self.other_company_brand
        new_invoice._onchange_brand_id()
        self.assertEqual(new_invoice.company_id, self.other_company)

    def test_get_view(self):
        view = self.env["account.move"].get_view(
            view_id=self.env.ref("account.view_move_form").id,
            view_type="form",
        )
        doc = etree.XML(view["arch"])
        self.assertTrue(doc.xpath("//field[@name='brand_use_level']"))

    def test_reverse_move(self):
        move = self.env["account.move"].create(
            {
                "name": "Sample invoice",
                "move_type": "out_invoice",
                "company_id": self.company.id,
                "journal_id": self.journal.id,
                "partner_id": self.partner.id,
                "brand_id": self.brand.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.env.ref("product.product_product_1").id,
                            "quantity": 40.0,
                            "name": "product test 1",
                            "discount": 10.00,
                            "price_unit": 2.27,
                        },
                    )
                ],
            }
        )
        move.action_post()
        reverse_wizard = Form(
            self.env["account.move.reversal"].with_context(
                active_ids=move.ids, active_model="account.move"
            )
        )
        reverse_wizard.reason = "modify"
        reverse = reverse_wizard.save()
        action = reverse.reverse_moves()
        credit_note = self.env["account.move"].browse(action.get("res_id"))
        self.assertEqual(credit_note.brand_id, self.brand)

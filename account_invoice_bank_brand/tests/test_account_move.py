# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon


class TestAccountInvoiceBankBrand(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Sale Journal",
                "code": "SALE",
                "type": "sale",
                "company_id": cls.company.id,
            }
        )
        cls.invoice = cls.env["account.move"].create(
            {
                "partner_id": cls.partner.id,
                "move_type": "out_invoice",
                "company_id": cls.company.id,
                "partner_bank_id": False,  # Explicitly set to False
            }
        )
        cls.partner_bank = cls.env["res.partner.bank"].create(
            {
                "partner_id": cls.partner.id,
                "acc_number": "NL1234567890",
                "company_id": cls.company.id,
            }
        )
        cls.brand = cls.env["res.brand"].create(
            {
                "name": "Test Brand",
                "partner_id": cls.partner.id,
                "company_id": cls.company.id,
            }
        )

    def test_brand_compute_partner_bank_id(self):
        # 1. Set brand_id on invoice
        self.invoice.brand_id = self.brand
        # 2. Assert partner_bank_id is set if brand has it
        self.brand.partner_bank_id = self.partner_bank
        # Trigger recompute
        self.invoice._compute_partner_bank_id()
        self.assertEqual(self.invoice.partner_bank_id, self.brand.partner_bank_id)

    def test_create_invoice_with_brand(self):
        self.brand.partner_bank_id = self.partner_bank
        invoice = self.env["account.move"].create(
            {
                "partner_id": self.partner.id,
                "move_type": "out_invoice",
                "brand_id": self.brand.id,
                "company_id": self.company.id,
            }
        )
        self.assertEqual(invoice.partner_bank_id, self.brand.partner_bank_id)

    def test_validate_partner_bank_id_constraint(self):
        # 1. Create a bank account for a different partner
        another_partner = self.env["res.partner"].create({"name": "Another Partner"})
        another_partner_bank = self.env["res.partner.bank"].create(
            {
                "partner_id": another_partner.id,
                "acc_number": "OTHER123",
                "company_id": self.company.id,
            }
        )

        # 2. Expect a ValidationError when assigning the invalid bank account
        with self.assertRaises(ValidationError):
            self.brand.partner_bank_id = another_partner_bank

        # 3. Assign a valid bank account (this should work)
        self.brand.partner_bank_id = self.partner_bank
        self.brand.validate_partner_bank_id()

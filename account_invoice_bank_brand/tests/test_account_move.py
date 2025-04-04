# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestAccountInvoiceBankBrand(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.res_partner_12")  # A customer partner
        cls.company = cls.env.ref("base.main_company")
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

    def test_onchange_brand(self):
        # 1. Initially, partner_bank_id should be False
        self.assertFalse(self.invoice.partner_bank_id)
        # 2. Set brand_id on invoice
        self.invoice.brand_id = self.brand
        # 3. Trigger onchange
        self.invoice._onchange_brand()
        # 4. Assert partner_bank_id is set if brand has it
        self.brand.partner_bank_id = self.partner_bank
        self.invoice.brand_id = self.brand
        self.invoice._onchange_brand()
        self.assertEqual(self.invoice.partner_bank_id, self.brand.partner_bank_id)

    def test_create_invoice_with_brand(self):
        self.brand.partner_bank_id = self.partner_bank
        invoice = self.env["account.move"].create(
            {
                "partner_id": self.partner.id,
                "move_type": "out_invoice",
                "brand_id": self.brand.id,
                "company_id": self.company.id,
                "partner_bank_id": self.partner_bank.id,
            }
        )
        self.assertEqual(invoice.partner_bank_id, self.brand.partner_bank_id)

    def test_validate_partner_bank_id_constraint(self):
        # 1. Create a bank account for a different partner
        another_partner = self.env.ref("base.res_partner_2")
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

# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestBasePaymentModeBrand(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.manual_out = cls.env.ref("account.account_payment_method_manual_out")
        cls.company = cls.env.user.company_id
        cls.journal_1 = cls.env["account.journal"].create(
            {
                "name": "J1",
                "code": "J1",
                "type": "bank",
                "company_id": cls.company.id,
                "bank_acc_number": "123456",
            }
        )
        cls.payment_mode_1 = cls.env["account.payment.mode"].create(
            {
                "name": "Customer To Bank 1",
                "bank_account_link": "variable",
                "payment_method_id": cls.manual_out.id,
                "show_bank_account_from_journal": True,
                "company_id": cls.company.id,
                "fixed_journal_id": cls.journal_1.id,
                "variable_journal_ids": [(6, 0, [cls.journal_1.id])],
            }
        )
        cls.payment_mode_2 = cls.env["account.payment.mode"].create(
            {
                "name": "Customer To Bank 2",
                "bank_account_link": "variable",
                "payment_method_id": cls.manual_out.id,
                "show_bank_account_from_journal": True,
                "company_id": cls.company.id,
                "fixed_journal_id": cls.journal_1.id,
                "variable_journal_ids": [(6, 0, [cls.journal_1.id])],
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Customer",
                "customer_payment_mode_id": cls.payment_mode_1.id,
            }
        )
        cls.brand = cls.env["res.brand"].create({"name": "brand"})
        cls.brand.allowed_payment_mode_ids = cls.payment_mode_1


class TestAccountPaymentModeBrand(TestBasePaymentModeBrand):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.invoice = cls.env["account.move"].create(
            {"partner_id": cls.partner.id, "brand_id": cls.brand.id}
        )

    def test_account_invoice_allowed_payment_mode(self):
        self.assertEqual(self.invoice.allowed_payment_mode_ids, self.payment_mode_1)
        self.invoice.brand_id = False
        self.assertEqual(
            self.invoice.allowed_payment_mode_ids,
            self.env["account.payment.mode"].search([]),
        )

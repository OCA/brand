# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestBasePaymentModeBrand(TransactionCase):
    def setUp(self):
        super(TestBasePaymentModeBrand, self).setUp()
        self.manual_out = self.env.ref(
            "account.account_payment_method_manual_out"
        )
        self.company = self.env.user.company_id
        self.journal_1 = self.env["account.journal"].create(
            {
                "name": "J1",
                "code": "J1",
                "type": "bank",
                "company_id": self.company.id,
                "bank_acc_number": "123456",
            }
        )
        self.payment_mode_1 = self.env["account.payment.mode"].create(
            {
                "name": "Customer To Bank 1",
                "bank_account_link": "variable",
                "payment_method_id": self.manual_out.id,
                "show_bank_account_from_journal": True,
                "company_id": self.company.id,
                "fixed_journal_id": self.journal_1.id,
                "variable_journal_ids": [(6, 0, [self.journal_1.id])],
            }
        )
        self.payment_mode_2 = self.env["account.payment.mode"].create(
            {
                "name": "Customer To Bank 2",
                "bank_account_link": "variable",
                "payment_method_id": self.manual_out.id,
                "show_bank_account_from_journal": True,
                "company_id": self.company.id,
                "fixed_journal_id": self.journal_1.id,
                "variable_journal_ids": [(6, 0, [self.journal_1.id])],
            }
        )
        self.partner = self.env["res.partner"].create(
            {
                "name": "Customer",
                "customer_payment_mode_id": self.payment_mode_1.id,
            }
        )
        self.brand = self.env["res.brand"].create({"name": "brand"})
        self.brand.allowed_payment_mode_ids = self.payment_mode_1


class TestAccountPaymentModeBrand(TestBasePaymentModeBrand):
    def setUp(self):
        super(TestAccountPaymentModeBrand, self).setUp()
        self.invoice = self.env["account.invoice"].create(
            {"partner_id": self.partner.id, "brand_id": self.brand.id}
        )

    def test_account_invoice_allowed_payment_mode(self):
        self.assertEqual(
            self.invoice.allowed_payment_mode_ids, self.payment_mode_1
        )
        self.invoice.brand_id = False
        self.assertEqual(
            self.invoice.allowed_payment_mode_ids,
            self.env['account.payment.mode'].search([]),
        )

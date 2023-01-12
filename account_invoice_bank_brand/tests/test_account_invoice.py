# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestAccountInvoice(SavepointCase):
    def setUp(self):
        super(TestAccountInvoice, self).setUp()
        self.partner_id = self.env.ref("base.res_partner_12")
        self.invoice = self.env["account.invoice"].create(
            {"partner_id": self.partner_id.id, "type": "out_invoice"}
        )
        company_id = self.env["res.company"].browse(1)
        self.partner_bank_id = self.env["res.partner.bank"].create(
            {"acc_number": "123456", "partner_id": company_id.partner_id.id}
        )
        self.brand_id = self.env["res.brand"].create(
            {
                "name": "Brand",
                "partner_bank_id": self.partner_bank_id.id,
                "company_id": 1,
            }
        )

    def test_on_change_brand_id(self):
        self.invoice._onchange_brand()
        self.assertNotEqual(self.invoice.partner_bank_id, self.partner_bank_id)
        self.invoice.brand_id = self.brand_id
        self.invoice._onchange_brand()
        self.assertEqual(self.invoice.partner_bank_id, self.partner_bank_id)

    def test_create_invoice(self):
        invoice = self.env["account.invoice"].create(
            {
                "partner_id": self.partner_id.id,
                "type": "out_invoice",
                "brand_id": self.brand_id.id,
            }
        )
        self.assertEqual(invoice.partner_bank_id, self.partner_bank_id)

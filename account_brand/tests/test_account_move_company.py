# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountMoveCompany(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_data_2 = cls.setup_other_company()

    def test_invoice_company_from_journal(self):
        """An invoice created with the journal of another company belongs to
        that company"""
        journal = self.company_data_2["default_journal_sale"]
        invoice = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "invoice_date": "2017-01-01",
                "partner_id": self.partner_a.id,
                "journal_id": journal.id,
            }
        )
        self.assertEqual(invoice.company_id, self.company_data_2["company"])

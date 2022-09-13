# Copyright 2022 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SavepointCase


class TestAccountMove(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.Brand = cls.env["res.brand"]
        cls.AccountMove = cls.env["account.move"]
        cls.AccountAccount = cls.env["account.account"]
        cls.StockMove = cls.env["stock.move"]
        cls.SaleOrder = cls.env["sale.order"]
        cls.Picking = cls.env["stock.picking"]
        cls.partner = cls.env.ref("base.res_partner_12")
        cls.product = cls.env.ref("product.product_product_4")
        cls.account_type = cls.env.ref("account.data_account_type_revenue")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.picking_type_out = cls.env.ref("stock.picking_type_out")
        cls.brand = cls.Brand.create({"name": "Brand"})
        cls.brand2 = cls.Brand.create({"name": "Brand 2"})
        cls.account = cls.AccountAccount.create(
            {
                "name": "Test sale",
                "code": "XX_700",
                "user_type_id": cls.account_type.id,
            }
        )
        cls.sale = cls.SaleOrder.create(
            {
                "partner_id": cls.partner.id,
                "brand_id": cls.brand.id,
                "order_line": [
                    (
                        0,
                        False,
                        {
                            "product_id": cls.product.id,
                        },
                    )
                ],
            }
        )
        cls.picking = cls.Picking.create(
            {
                "sale_id": cls.sale.id,
                "picking_type_id": cls.picking_type_out.id,
                "location_id": cls.stock_location.id,
                "location_dest_id": cls.customer_location.id,
                "move_ids_without_package": [
                    (
                        0,
                        False,
                        {
                            "product_id": cls.product.id,
                            "name": cls.product.display_name,
                            "product_uom": cls.product.uom_id.id,
                        },
                    )
                ],
            }
        )
        cls.stock_move = cls.picking.move_lines

    def test_create_with_brand(self):
        """
        When the stock_move_id is specified (but not the brand_id)
        during account.move creation, it should auto-fill the brand_id
        with the one set on the stock_move.picking_id.sale_id.brand_id
        """
        account_move = self.AccountMove.create(
            {
                "partner_id": self.partner.id,
                "type": "out_invoice",
                "stock_move_id": self.stock_move.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 42,
                            "name": "something",
                            "account_id": self.account.id,
                        },
                    )
                ],
            }
        )
        self.assertEqual(
            account_move.brand_id, self.stock_move.picking_id.sale_id.brand_id
        )

    def test_create_without_brand(self):
        """
        In this case, the brand is not set on the sale order so it shouldn't fill
        it on the account.move.
        """
        self.stock_move.picking_id.sale_id.write({"brand_id": False})
        account_move = self.AccountMove.create(
            {
                "partner_id": self.partner.id,
                "type": "out_invoice",
                "stock_move_id": self.stock_move.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 42,
                            "name": "something",
                            "account_id": self.account.id,
                        },
                    )
                ],
            }
        )
        self.assertFalse(account_move.brand_id)

    def test_create_with_brand_filled(self):
        """
        In this case we specify manually (in the create) so the brand_id should
        be forced by the one set on the related sale order.
        """
        account_move = self.AccountMove.create(
            {
                "partner_id": self.partner.id,
                "type": "out_invoice",
                "stock_move_id": self.stock_move.id,
                "brand_id": self.brand2.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": 42,
                            "name": "something",
                            "account_id": self.account.id,
                        },
                    )
                ],
            }
        )
        self.assertEqual(account_move.brand_id, self.brand2)

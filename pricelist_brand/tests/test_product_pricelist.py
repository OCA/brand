# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import float_compare


class TestProductPricelist(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_brand_obj = cls.env["product.brand"]
        cls.product_brand = cls.env["product.brand"].create(
            {"name": "Test Brand", "description": "Test brand description"}
        )
        cls.product_categ = cls.env["product.category"].create(
            {"name": "Test Category"}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product 1",
                "lst_price": 100.0,
                "product_brand_id": cls.product_brand.id,
                "categ_id": cls.product_categ.id,
            }
        )
        cls.product_2 = cls.env["product.product"].create(
            {
                "name": "Test Product 2",
                "lst_price": 200.0,
                "categ_id": cls.product_categ.id,
            }
        )

        cls.list0 = cls.env["product.pricelist"].create({"name": "Public Pricelist"})
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test Pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Default pricelist",
                            "compute_price": "formula",
                            "base": "pricelist",
                            "base_pricelist_id": cls.list0.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "10% Discount on Test Brand",
                            "applied_on": "25_brand",
                            "product_brand_id": cls.product_brand.id,
                            "compute_price": "formula",
                            "base": "list_price",
                            "price_discount": 10,
                        },
                    ),
                ],
            }
        )

    def test_ensure_pricelist_item_consistency(self):
        with self.assertRaises(ValidationError):
            self.env["product.pricelist.item"].create(
                {
                    "pricelist_id": self.pricelist.id,
                    "base": "list_price",
                    "compute_price": "formula",
                    "applied_on": "25_brand",
                }
            )
        pricelist_item = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "base": "list_price",
                "compute_price": "formula",
                "applied_on": "25_brand",
                "product_brand_id": self.product_brand.id,
            }
        )
        pricelist_item.write({"product_brand_id": self.product_brand.id})
        pricelist_item._compute_name()
        self.assertEqual(
            pricelist_item.name,
            self.env._("Brand: %s", self.product_brand.display_name),
        )
        pricelist_item_2 = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "base": "list_price",
                "compute_price": "formula",
                "applied_on": "2_product_category",
                "categ_id": self.product_categ.id,
                "product_brand_id": self.product_brand.id,
            }
        )
        self.assertFalse(pricelist_item_2.product_brand_id)
        pricelist_item_3 = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "base": "list_price",
                "compute_price": "formula",
                "applied_on": "1_product",
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "product_brand_id": self.product_brand.id,
            }
        )
        self.assertFalse(pricelist_item_3.product_brand_id)
        pricelist_item_4 = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "base": "list_price",
                "compute_price": "formula",
                "applied_on": "0_product_variant",
                "product_id": self.product.id,
                "product_brand_id": self.product_brand.id,
            }
        )
        self.assertFalse(pricelist_item_4.product_brand_id)
        self.assertFalse(
            any(
                [
                    pricelist_item.product_id,
                    pricelist_item.product_tmpl_id,
                    pricelist_item.categ_id,
                ]
            )
        )
        pricelist_item.write(
            {"applied_on": "0_product_variant", "product_id": self.product.id}
        )
        self.assertFalse(pricelist_item.product_brand_id)
        pricelist_item.write(
            {"applied_on": "25_brand", "product_brand_id": self.product_brand.id}
        )
        self.assertFalse(pricelist_item.product_id)
        pricelist_item.write(
            {
                "applied_on": "1_product",
                "product_tmpl_id": self.product.product_tmpl_id.id,
            }
        )
        self.assertFalse(pricelist_item.product_brand_id)
        pricelist_item.write(
            {"applied_on": "25_brand", "product_brand_id": self.product_brand.id}
        )
        self.assertFalse(pricelist_item.product_tmpl_id)
        pricelist_item.write(
            {"applied_on": "2_product_category", "categ_id": self.product.categ_id.id}
        )
        self.assertFalse(pricelist_item.product_brand_id)
        pricelist_item.write(
            {"applied_on": "25_brand", "product_brand_id": self.product_brand.id}
        )
        self.assertFalse(pricelist_item.categ_id)
        pricelist_item.write({"applied_on": "3_global"})
        self.assertFalse(pricelist_item.product_brand_id)

        # Line 117: Create with 3_global
        pricelist_item_global = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "base": "list_price",
                "compute_price": "formula",
                "applied_on": "3_global",
                "product_brand_id": self.product_brand.id,
            }
        )
        self.assertFalse(pricelist_item_global.product_brand_id)

        # Lines 85-96: _onchange_display_applied_on
        item_onchange_1 = self.env["product.pricelist.item"].new({})
        item_onchange_1.display_applied_on = "25_brand"
        item_onchange_1._onchange_display_applied_on()
        self.assertEqual(item_onchange_1.applied_on, "25_brand")
        self.assertFalse(item_onchange_1.product_id)

        # Lines 100-104: _onchange_rule_content
        item_onchange_2 = self.env["product.pricelist.item"].new({})
        item_onchange_2.product_brand_id = self.product_brand.id
        item_onchange_2._onchange_rule_content()
        self.assertEqual(item_onchange_2.applied_on, "25_brand")

    def test_calculation_price_of_products_pricelist(self):
        """Test calculation of product price based on pricelist"""
        # Check sale price of branded product
        product_with_context = self.product.with_context(
            pricelist=self.pricelist.id, quantity=1
        )
        self.assertEqual(
            float_compare(
                product_with_context._get_contextual_price(),
                (
                    product_with_context.lst_price
                    - product_with_context.lst_price * (0.10)
                ),
                precision_digits=2,
            ),
            0,
        )

        # Check sale price of not branded product (should not change)
        product_2_with_context = self.product_2.with_context(
            pricelist=self.pricelist.id, quantity=1
        )
        self.assertEqual(
            float_compare(
                product_2_with_context._get_contextual_price(),
                product_2_with_context.lst_price,
                precision_digits=2,
            ),
            0,
        )

        # Line 15: Check sale price using product.template instead of product.product
        template_with_context = self.product.product_tmpl_id.with_context(
            pricelist=self.pricelist.id, quantity=1
        )
        self.assertEqual(
            float_compare(
                template_with_context._get_contextual_price(),
                (
                    template_with_context.list_price
                    - template_with_context.list_price * (0.10)
                ),
                precision_digits=2,
            ),
            0,
        )

        # Lines 55 and 58: _is_applicable_for
        brand_item = self.pricelist.item_ids.filtered(
            lambda x: x.applied_on == "25_brand"
        )

        # Line 58: test template
        self.assertTrue(
            brand_item._is_applicable_for(self.product.product_tmpl_id, 1.0)
        )

        # Line 55: super() returns False
        brand_item.min_quantity = 5.0
        self.assertFalse(brand_item._is_applicable_for(self.product, 1.0))

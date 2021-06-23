# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import exceptions

from odoo.addons.product_brand.tests.common import CommonCase


class TestBrandTags(CommonCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_brand2 = cls.product_brand.copy({"name": "Test Brand 2"})
        cls.product_brand3 = cls.product_brand.copy({"name": "Test Brand 3"})
        cls.tag = cls.env["product.brand.tag"].create(
            {
                "name": "Test Tag",
                "product_brand_ids": [(6, 0, [cls.product_brand3.id])],
                "secondary_product_brand_ids": [
                    (6, 0, [cls.product_brand.id, cls.product_brand2.id])
                ],
            }
        )

    def test_brand_rel(self):
        self.assertEqual(self.product_brand.secondary_tag_ids, self.tag)
        self.assertEqual(self.product_brand2.secondary_tag_ids, self.tag)
        self.assertEqual(self.product_brand3.tag_ids, self.tag)

    def test_brand_rel_check(self):
        with self.assertRaisesRegex(
            exceptions.UserError, self.tag._check_brands_relation_error_msg(self.tag)
        ):
            self.tag.secondary_product_brand_ids += self.product_brand3

    def test_count(self):
        self.assertEqual(self.tag.secondary_brands_count, 2)
        self.tag.secondary_product_brand_ids -= self.product_brand2
        self.assertEqual(self.tag.secondary_brands_count, 1)

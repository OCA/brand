# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestBrandExternalReportLayout(TransactionCase):
    def setUp(self):
        super(TestBrandExternalReportLayout, self).setUp()
        self.brand = self.env["res.brand"].create({"name": "brand"})

    def test_get_default_brand_logo(self):
        self.assertEqual(self.brand.logo, self.brand._get_default_brand_logo())

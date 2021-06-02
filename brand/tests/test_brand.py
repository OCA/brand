# Copyright 2017 ForgeFlow S.L.
# Copyright 2017 Luxim d.o.o.
# Copyright 2017 Matmoz d.o.o.
# Copyright 2017 Deneroteam.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# Copyright 2017 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from odoo.addons.brand.models.res_company import (
    BRAND_USE_LEVEL_NO_USE_LEVEL,
    BRAND_USE_LEVEL_REQUIRED_LEVEL,
    BRAND_USE_LEVEL_SELECTION,
)


class TestBrand(TransactionCase):
    def setUp(self):
        super(TestBrand, self).setUp()
        self.company = self.env.ref("base.main_company")
        self.company.brand_use_level = "required"
        print("dddddddddddddddddddDDDDDDDD")

        self.res_brand_mixin = self.env["res.brand.mixin"]

    def test_check_brand_requirement(self):
        brand_mixin_id = self.res_brand_mixin.create({
            'brand_use_level' : "required",
            'company_id' : self.company.id
        })
        self.assertRaises(ValidationError)
            

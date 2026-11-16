from odoo.exceptions import AccessError
from odoo.tests.common import new_test_user

from .common import CommonCase


class TestBrandMixin(CommonCase):
    def test_brand_creation(self):
        """Test creation of a brand."""
        brand = self.brand_model.create({"partner_id": self.partner.id})
        self.assertTrue(brand.exists())

    def test_brand_access_and_company_restriction(self):
        user = new_test_user(
            self.env,
            login="brand_reader",
            company_id=self.company_optional_brand.id,
            company_ids=[(6, 0, self.company_optional_brand.ids)],
        )
        own_brand = self.brand_model.create(
            {"name": "Own brand", "company_id": self.company_optional_brand.id}
        )
        other_brand = self.brand_model.create(
            {"name": "Other brand", "company_id": self.company_no_brand.id}
        )
        self.assertTrue(self.brand.with_user(user).has_access("read"))
        self.assertTrue(own_brand.with_user(user).has_access("read"))
        self.assertFalse(other_brand.with_user(user).has_access("read"))
        with self.assertRaises(AccessError):
            own_brand.with_user(user).write({"name": "Forbidden change"})

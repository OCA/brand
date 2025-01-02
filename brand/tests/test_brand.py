from .common import CommonCase


class TestBrandMixin(CommonCase):
    def test_brand_creation(self):
        """Test creation of a brand."""
        brand = self.brand_model.create({"partner_id": self.partner.id})
        self.assertTrue(brand.exists())

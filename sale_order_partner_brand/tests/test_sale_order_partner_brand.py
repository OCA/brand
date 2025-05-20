import logging

from odoo.tests import common, tagged

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install", "sale_order_partner_brand")
class TestSaleOrderPartnerBrand(common.TransactionCase):
    """
    Test cases for the sale_order_partner_brand module.
    Verifies that the brand_id on a Sales Order is correctly updated
    when the partner_id changes, based on the partner's or its
    commercial entity's assigned brand.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # Models
        cls.ResPartner = cls.env["res.partner"]
        cls.ResBrand = cls.env["res.brand"]
        cls.SaleOrder = cls.env["sale.order"]
        cls.ProductProduct = cls.env["product.product"]

        # Create Brands
        cls.brand_a = cls.ResBrand.create({"name": "Test Brand A"})
        cls.brand_b = cls.ResBrand.create({"name": "Test Brand B"})
        cls.brand_c = cls.ResBrand.create({"name": "Test Brand C (Child Only)"})

        # Create Partners
        # Scenario 1: Parent company with a brand
        cls.parent_co_with_brand_a = cls.ResPartner.create(
            {
                "name": "Parent Co (Brand A)",
                "is_company": True,
                "brand_id": cls.brand_a.id,
            }
        )
        cls.child_contact_of_parent_a = cls.ResPartner.create(
            {
                "name": "Child Contact of Parent A (No Brand)",
                "parent_id": cls.parent_co_with_brand_a.id,
                "type": "contact",
            }
        )
        cls.child_contact_of_parent_a_with_own_brand_b = cls.ResPartner.create(
            {
                "name": "Child Contact of Parent A (Own Brand B)",
                "parent_id": cls.parent_co_with_brand_a.id,
                "type": "contact",
                "brand_id": cls.brand_b.id,
            }
        )

        # Scenario 2: Parent company without a brand
        cls.parent_co_no_brand = cls.ResPartner.create(
            {"name": "Parent Co (No Brand)", "is_company": True}
        )
        cls.child_contact_of_parent_no_brand_with_brand_c = cls.ResPartner.create(
            {
                "name": "Child Contact of Parent NoBrand (Own Brand C)",
                "parent_id": cls.parent_co_no_brand.id,
                "type": "contact",
                "brand_id": cls.brand_c.id,
            }
        )
        cls.child_contact_of_parent_no_brand_no_brand = cls.ResPartner.create(
            {
                "name": "Child Contact of Parent NoBrand (No Brand)",
                "parent_id": cls.parent_co_no_brand.id,
                "type": "contact",
            }
        )

        # Scenario 3: Standalone partner (company or individual) with a brand
        cls.standalone_partner_with_brand_b = cls.ResPartner.create(
            {"name": "Standalone Customer (Brand B)", "brand_id": cls.brand_b.id}
        )

        # Scenario 4: Standalone partner without a brand
        cls.standalone_partner_without_brand = cls.ResPartner.create(
            {"name": "Standalone Customer (No Brand)"}
        )

        cls.product_test = cls.ProductProduct.create(
            {"name": "Test Product for SO", "type": "service"}
        )
        _logger.info("TestSaleOrderPartnerBrand: setUpClass completed.")

    def _trigger_onchange_partner(self, order_form, partner_record):
        """Helper to simulate partner change and trigger onchange."""
        order_form.partner_id = partner_record
        order_form._onchange_partner_id_set_brand()

    def test_01_onchange_partner_is_company_with_brand(self):
        """Onchange: Partner is a company with its own brand."""
        _logger.debug("Running test_01_onchange_partner_is_company_with_brand...")
        order_form = self.SaleOrder.new({})
        self._trigger_onchange_partner(order_form, self.parent_co_with_brand_a)
        self.assertEqual(
            order_form.brand_id,
            self.brand_a,
            "SO brand should match the company's brand (Brand A).",
        )

    def test_02_onchange_partner_is_child_parent_has_brand(self):
        """Onchange: Partner is child, parent company has brand."""
        _logger.debug("Running test_02_onchange_partner_is_child_parent_has_brand...")
        order_form = self.SaleOrder.new({})
        self._trigger_onchange_partner(order_form, self.child_contact_of_parent_a)
        self.assertEqual(
            order_form.brand_id,
            self.brand_a,
            "SO brand should match the parent company's brand (Brand A).",
        )

    def test_03_onchange_child_has_own_brand_parent_has_brand(self):
        """Onchange: Child has own brand, parent also has brand. Parent's wins."""
        _logger.debug(
            "Running test_03_onchange_child_has_own_brand_parent_has_brand..."
        )
        order_form = self.SaleOrder.new({})
        self._trigger_onchange_partner(
            order_form, self.child_contact_of_parent_a_with_own_brand_b
        )
        self.assertEqual(
            order_form.brand_id,
            self.brand_a,  # Parent (commercial_partner_id) brand takes precedence
            "SO brand should match parent's brand (A), not child's (B).",
        )

    def test_04_onchange_child_has_brand_parent_no_brand(self):
        """Onchange: Child has brand, parent company has no brand. Child's used."""
        _logger.debug("Running test_04_onchange_child_has_brand_parent_no_brand...")
        order_form = self.SaleOrder.new({})
        self._trigger_onchange_partner(
            order_form, self.child_contact_of_parent_no_brand_with_brand_c
        )
        self.assertEqual(
            order_form.brand_id,
            self.brand_c,  # Fallback to child's brand
            "SO brand should match child's brand (Brand C) as parent has none.",
        )

    def test_05_onchange_partner_no_brand_parent_no_brand(self):
        """Onchange: Neither partner nor its parent has a brand."""
        _logger.debug("Running test_05_onchange_partner_no_brand_parent_no_brand...")
        order_form_standalone = self.SaleOrder.new({})
        self._trigger_onchange_partner(
            order_form_standalone, self.standalone_partner_without_brand
        )
        self.assertFalse(
            order_form_standalone.brand_id,
            "Brand should be cleared for standalone partner without brand.",
        )
        order_form_child = self.SaleOrder.new({})
        self._trigger_onchange_partner(
            order_form_child, self.child_contact_of_parent_no_brand_no_brand
        )
        self.assertFalse(
            order_form_child.brand_id,
            "Brand should be cleared for child whose parent also has no brand.",
        )

    def test_06_onchange_partner_cleared(self):
        """Onchange: Brand is cleared when partner is removed."""
        _logger.debug("Running test_06_onchange_partner_cleared...")
        order_form = self.SaleOrder.new({})
        self._trigger_onchange_partner(order_form, self.parent_co_with_brand_a)
        self.assertEqual(order_form.brand_id, self.brand_a)

        self._trigger_onchange_partner(order_form, False)  # Clear partner
        self.assertFalse(order_form.brand_id, "Brand should be cleared.")

    def test_07_create_so_with_child_partner_parent_has_brand(self):
        """Create: SO with child contact, parent company has brand."""
        _logger.debug(
            "Running test_07_create_so_with_child_partner_parent_has_brand..."
        )
        order = self.SaleOrder.create(
            {
                "partner_id": self.child_contact_of_parent_a.id,
                "order_line": [
                    (0, 0, {"product_id": self.product_test.id, "product_uom_qty": 1})
                ],
            }
        )
        self.assertEqual(
            order.brand_id, self.brand_a, "SO brand should match parent's brand."
        )

    def test_08_create_so_child_has_brand_parent_has_brand(self):
        """Create: SO with child (has brand), parent (has brand). Parent's wins."""
        _logger.debug("Running test_08_create_so_child_has_brand_parent_has_brand...")
        order = self.SaleOrder.create(
            {
                "partner_id": self.child_contact_of_parent_a_with_own_brand_b.id,
                "order_line": [
                    (0, 0, {"product_id": self.product_test.id, "product_uom_qty": 1})
                ],
            }
        )
        self.assertEqual(
            order.brand_id, self.brand_a, "SO brand should match parent's brand."
        )

    def test_09_create_so_child_has_brand_parent_no_brand(self):
        """Create: SO with child (has brand), parent (no brand). Child's used."""
        _logger.debug("Running test_09_create_so_child_has_brand_parent_no_brand...")
        order = self.SaleOrder.create(
            {
                "partner_id": self.child_contact_of_parent_no_brand_with_brand_c.id,
                "order_line": [
                    (0, 0, {"product_id": self.product_test.id, "product_uom_qty": 1})
                ],
            }
        )
        self.assertEqual(
            order.brand_id, self.brand_c, "SO brand should match child's brand."
        )

    def test_10_create_so_partner_no_brand_parent_no_brand(self):
        """Create: SO with partner (no brand), parent (no brand). No brand set."""
        _logger.debug("Running test_10_create_so_partner_no_brand_parent_no_brand...")
        order = self.SaleOrder.create(
            {
                "partner_id": self.child_contact_of_parent_no_brand_no_brand.id,
                "order_line": [
                    (0, 0, {"product_id": self.product_test.id, "product_uom_qty": 1})
                ],
            }
        )
        self.assertFalse(order.brand_id, "SO brand should be empty.")

    def test_11_create_so_standalone_partner_with_brand(self):
        """Create: SO with standalone partner having a brand."""
        _logger.debug("Running test_11_create_so_standalone_partner_with_brand...")
        order = self.SaleOrder.create(
            {
                "partner_id": self.standalone_partner_with_brand_b.id,
                "order_line": [
                    (0, 0, {"product_id": self.product_test.id, "product_uom_qty": 1})
                ],
            }
        )
        self.assertEqual(
            order.brand_id, self.brand_b, "SO brand should match partner's brand."
        )

    def test_12_create_so_standalone_partner_no_brand(self):
        """Create: SO with standalone partner having no brand."""
        _logger.debug("Running test_12_create_so_standalone_partner_no_brand...")
        order = self.SaleOrder.create(
            {
                "partner_id": self.standalone_partner_without_brand.id,
                "order_line": [
                    (0, 0, {"product_id": self.product_test.id, "product_uom_qty": 1})
                ],
            }
        )
        self.assertFalse(order.brand_id, "SO brand should be empty.")

    def test_13_create_so_with_explicit_brand_overrides_partner_logic(self):
        """Create: SO with explicit brand_id in vals should use that."""
        _logger.debug(
            "Running test_13_create_so_with_explicit_brand_overrides_partner_logic..."
        )
        order = self.SaleOrder.create(
            {
                "partner_id": self.parent_co_with_brand_a.id,
                "brand_id": self.brand_b.id,  # Explicitly provide brand_b
                "order_line": [
                    (0, 0, {"product_id": self.product_test.id, "product_uom_qty": 1})
                ],
            }
        )
        self.assertEqual(
            order.brand_id,
            self.brand_b,
            "Explicitly provided brand_id should override partner-derived brand.",
        )

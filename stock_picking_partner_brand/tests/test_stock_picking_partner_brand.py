import logging

from odoo.tests import common, tagged

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install", "stock_picking_partner_brand")
class TestStockPickingPartnerBrand(common.TransactionCase):
    """
    Test cases for the stock_picking_partner_brand module.
    Verifies that the brand_id on a Stock Picking is correctly updated
    when the partner_id changes, based on the partner's or commercial partner's
    assigned brand.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # Models
        cls.ResPartner = cls.env["res.partner"]
        cls.ResBrand = cls.env["res.brand"]
        cls.StockPicking = cls.env["stock.picking"]
        cls.StockPickingType = cls.env["stock.picking.type"]
        cls.ProductProduct = cls.env["product.product"]

        # Create Brands
        cls.brand_alpha = cls.ResBrand.create({"name": "Test Brand Alpha"})
        cls.brand_beta = cls.ResBrand.create({"name": "Test Brand Beta"})

        # Create Partners
        cls.parent_company_with_brand_alpha = cls.ResPartner.create(
            {
                "name": "Parent Co Alpha",
                "is_company": True,
                "brand_id": cls.brand_alpha.id,
            }
        )
        cls.child_contact_of_alpha = cls.ResPartner.create(
            {
                "name": "Child Contact of Alpha",
                "parent_id": cls.parent_company_with_brand_alpha.id,
                "type": "contact",
                # This child contact intentionally does not have its own brand_id
            }
        )
        cls.standalone_partner_with_brand_beta = cls.ResPartner.create(
            {
                "name": "Standalone Customer Beta",
                "is_company": True,
                "brand_id": cls.brand_beta.id,
            }
        )
        cls.partner_without_brand = cls.ResPartner.create(
            {
                "name": "Customer Without Any Brand",
                "is_company": True,
            }
        )
        cls.child_contact_no_parent_brand = cls.ResPartner.create(
            {
                "name": "Child Contact, Parent No Brand",
                "parent_id": cls.partner_without_brand.id,
                "type": "contact",
            }
        )

        cls.picking_type_out = cls.env["stock.picking.type"].search(
            [
                ("code", "=", "outgoing"),
                ("warehouse_id.company_id", "=", cls.env.company.id),
            ],
            limit=1,
        )
        if not cls.picking_type_out:
            warehouse = cls.env["stock.warehouse"].search(
                [("company_id", "=", cls.env.company.id)], limit=1
            )
            if not warehouse:
                warehouse = cls.env["stock.warehouse"].create(
                    {
                        "name": "Test Warehouse",
                        "code": "TSTWH",
                        "company_id": cls.env.company.id,
                    }
                )
            cls.picking_type_out = cls.StockPickingType.create(
                {
                    "name": "Test Pickings Out",
                    "code": "outgoing",
                    "warehouse_id": warehouse.id,
                    "sequence_code": "TSTOUT",
                }
            )

        cls.product_generic = cls.ProductProduct.create(
            {"name": "Generic Product", "type": "consu"}
        )

        _logger.info("TestStockPickingPartnerBrand: setUpClass completed.")

    def _create_picking_form(self, partner_id=None):
        """
        Helper to simulate opening a new stock picking form with an optional partner.
        """
        vals = {"picking_type_id": self.picking_type_out.id}
        if partner_id:
            vals["partner_id"] = partner_id
        return self.StockPicking.new(vals)

    def test_01_onchange_child_contact_gets_parent_brand(self):
        """Test brand is set from parent company when a child contact is selected."""
        _logger.info("Running test_01_onchange_child_contact_gets_parent_brand...")

        picking_form = self._create_picking_form(
            partner_id=self.child_contact_of_alpha.id
        )
        picking_form._onchange_partner_id_set_brand()

        self.assertTrue(picking_form.brand_id, "Brand should be set on the picking.")
        self.assertEqual(
            picking_form.brand_id,
            self.parent_company_with_brand_alpha.brand_id,
            "Picking brand should match the parent company's brand.",
        )
        _logger.info("Test 01 Passed.")

    def test_02_onchange_standalone_partner_with_brand(self):
        """Test brand is set from a standalone partner who has a brand."""
        _logger.info("Running test_02_onchange_standalone_partner_with_brand...")

        picking_form = self._create_picking_form(
            partner_id=self.standalone_partner_with_brand_beta.id
        )
        picking_form._onchange_partner_id_set_brand()

        self.assertTrue(picking_form.brand_id, "Brand should be set on the picking.")
        self.assertEqual(
            picking_form.brand_id,
            self.standalone_partner_with_brand_beta.brand_id,
            "Picking brand should match the standalone partner's brand.",
        )
        _logger.info("Test 02 Passed.")

    def test_03_onchange_partner_without_brand_and_no_parent_brand(self):
        """Test brand is cleared if partner and its parent (if any) have no brand."""
        _logger.info(
            "Running test_03_onchange_partner_without_brand_and_no_" "parent_brand..."
        )

        # First, test with a standalone partner without a brand
        picking_form_no_brand_standalone = self._create_picking_form(
            partner_id=self.partner_without_brand.id
        )
        picking_form_no_brand_standalone._onchange_partner_id_set_brand()
        self.assertFalse(
            picking_form_no_brand_standalone.brand_id,
            "Brand should be cleared for standalone partner without brand.",
        )

        # Second, test with a child contact whose parent has no brand
        picking_form_no_brand_child = self._create_picking_form(
            partner_id=self.child_contact_no_parent_brand.id
        )
        picking_form_no_brand_child._onchange_partner_id_set_brand()
        self.assertFalse(
            picking_form_no_brand_child.brand_id,
            "Brand should be cleared for child contact whose parent has " "no brand.",
        )
        _logger.info("Test 03 Passed.")

    def test_04_onchange_partner_cleared(self):
        """Test brand is cleared when the partner is removed from the picking."""
        _logger.info("Running test_04_onchange_partner_cleared...")

        picking_form = self._create_picking_form(
            partner_id=self.parent_company_with_brand_alpha.id
        )
        picking_form._onchange_partner_id_set_brand()  # Set initial brand
        self.assertEqual(picking_form.brand_id, self.brand_alpha)

        # Clear the partner
        picking_form.partner_id = False
        picking_form._onchange_partner_id_set_brand()

        self.assertFalse(
            picking_form.brand_id, "Brand should be cleared when " "partner is removed."
        )
        _logger.info("Test 04 Passed.")

    def test_05_create_picking_with_child_partner_gets_parent_brand(self):
        """Test brand is set from parent during direct creation with a child partner."""
        _logger.info(
            "Running test_05_create_picking_with_child_partner_gets_" "parent_brand..."
        )
        picking = self.StockPicking.create(
            {
                "partner_id": self.child_contact_of_alpha.id,
                "picking_type_id": self.picking_type_out.id,
                "location_id": self.picking_type_out.default_location_src_id.id,
                "location_dest_id": self.picking_type_out.default_location_dest_id.id,
            }
        )
        self.assertTrue(picking.brand_id, "Brand should be set on picking creation.")
        self.assertEqual(
            picking.brand_id,
            self.parent_company_with_brand_alpha.brand_id,
            "Picking brand should match parent company's brand " "on creation.",
        )
        _logger.info("Test 05 Passed.")

    def test_06_create_picking_with_standalone_partner_with_brand(self):
        """Test brand is set during direct creation with a standalone partner having a "
        "brand."""
        _logger.info(
            "Running test_06_create_picking_with_standalone_" "partner_with_brand..."
        )
        picking = self.StockPicking.create(
            {
                "partner_id": self.standalone_partner_with_brand_beta.id,
                "picking_type_id": self.picking_type_out.id,
                "location_id": self.picking_type_out.default_location_src_id.id,
                "location_dest_id": self.picking_type_out.default_location_dest_id.id,
            }
        )
        self.assertTrue(picking.brand_id, "Brand should be set on picking creation.")
        self.assertEqual(
            picking.brand_id,
            self.standalone_partner_with_brand_beta.brand_id,
            "Picking brand should match standalone partner's brand on " "creation.",
        )
        _logger.info("Test 06 Passed.")

    def test_07_create_picking_with_partner_without_brand(self):
        """
        Test brand is not set during direct creation if partner (and parent)
        has no brand.
        """
        _logger.info("Running test_07_create_picking_with_partner_without_brand...")
        picking = self.StockPicking.create(
            {
                "partner_id": self.partner_without_brand.id,
                "picking_type_id": self.picking_type_out.id,
                "location_id": self.picking_type_out.default_location_src_id.id,
                "location_dest_id": self.picking_type_out.default_location_dest_id.id,
            }
        )
        self.assertFalse(
            picking.brand_id,
            "Brand should not be set if partner " "(and parent) has no brand.",
        )
        _logger.info("Test 07 Passed.")

    def test_08_create_picking_with_explicit_brand_overrides_partner_brand(self):
        """Test that an explicitly provided brand_id in create vals is respected."""
        _logger.info(
            "Running test_08_create_picking_with_explicit_brand_overrides_"
            "partner_brand..."
        )
        picking = self.StockPicking.create(
            {
                "partner_id": self.parent_company_with_brand_alpha.id,
                "brand_id": self.brand_beta.id,
                "picking_type_id": self.picking_type_out.id,
                "location_id": self.picking_type_out.default_location_src_id.id,
                "location_dest_id": self.picking_type_out.default_location_dest_id.id,
            }
        )
        self.assertTrue(picking.brand_id, "Brand should be set.")
        self.assertEqual(
            picking.brand_id,
            self.brand_beta,
            "Explicitly provided brand_id in create vals should override "
            "partner's brand.",
        )
        _logger.info("Test 08 Passed.")

    def test_09_create_picking_without_partner(self):
        """Test creating a picking without a partner_id."""
        _logger.info("Running test_09_create_picking_without_partner...")
        picking = self.StockPicking.create(
            {
                "picking_type_id": self.picking_type_out.id,
                "location_id": self.picking_type_out.default_location_src_id.id,
                "location_dest_id": self.picking_type_out.default_location_dest_id.id,
            }
        )
        self.assertFalse(
            picking.brand_id, "Brand should not be set if no partner " "is provided."
        )
        _logger.info("Test 09 Passed.")

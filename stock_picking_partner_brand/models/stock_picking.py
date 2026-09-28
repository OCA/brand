import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.onchange("partner_id")
    def _onchange_partner_id_set_brand(self):
        """
        Onchange method to set the brand_id on the Stock Picking
        based on the selected partner's brand or its parent company's brand.
        """
        brand_to_set = False

        if self.partner_id:
            # Determine the partner whose brand should be checked
            # Prefer the commercial entity (parent company) if it exists
            partner_for_brand_check = (
                self.partner_id.commercial_partner_id or self.partner_id
            )  # noqa

            if (
                hasattr(partner_for_brand_check, "brand_id")
                and partner_for_brand_check.brand_id
            ):  # noqa
                brand_to_set = partner_for_brand_check.brand_id
                _logger.info(
                    f"Stock Picking (virtual ID "
                    "{self._origin.id if self._origin else 'New'}): "
                    f"Partner '{self.partner_id.name}' selected. "
                    f"Using brand from '{partner_for_brand_check.name}': "
                    "'{brand_to_set.name}' (ID: {brand_to_set.id})."
                )
            else:
                _logger.info(
                    f"Stock Picking (virtual ID "
                    "{self._origin.id if self._origin else 'New'}): "
                    f"Partner '{self.partner_id.name}' selected. "
                    f"Neither partner nor its commercial entity "
                    "'{partner_for_brand_check.name}' has a brand. Clearing brand."
                )
        else:
            _logger.info(
                "Stock Picking (virtual ID "
                "{self._origin.id if self._origin else 'New'}): "
                "Partner cleared. Clearing brand."
            )

        # Set or clear the brand_id on the picking
        if hasattr(self, "brand_id"):
            self.brand_id = brand_to_set
        else:
            # This case should ideally not happen if stock_brand is correctly installed
            if self.partner_id:
                _logger.warning(
                    "Stock Picking model does not have a 'brand_id' field. "
                    "Is 'stock_brand' module installed and loaded correctly?"
                )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to ensure brand_id is set from partner_id
        (or its commercial entity)
        if provided during direct creation, and not already set in vals.
        """
        for vals in vals_list:
            # Only attempt to set brand_id if partner_id is provided and brand_id is not
            #  already in vals
            if vals.get("partner_id") and "brand_id" not in vals:
                partner = self.env["res.partner"].browse(vals.get("partner_id"))
                if partner.exists():
                    # Determine the partner whose brand should be checked
                    partner_for_brand_check = partner.commercial_partner_id or partner

                    if (
                        hasattr(partner_for_brand_check, "brand_id")
                        and partner_for_brand_check.brand_id
                    ):  # noqa
                        # Check if the stock.picking model (self) has brand_id field
                        if "brand_id" in self._fields:
                            vals["brand_id"] = partner_for_brand_check.brand_id.id
                            _logger.info(
                                f"Create Stock Picking: Partner"
                                " '{partner.name}' provided. "
                                f"Using brand from '{partner_for_brand_check.name}': "
                                "'{partner_for_brand_check.brand_id.name}'. "
                                f"Setting brand_id in creation vals."
                            )
                        else:
                            _logger.warning(
                                "Stock Picking model does not have a 'brand_id' "
                                "field during create. "
                                "Is 'stock_brand' module installed?"
                            )
                    else:
                        _logger.info(
                            f"Create Stock Picking: Partner '{partner.name}' provided. "
                            f"Neither partner nor its commercial entity "
                            "'{partner_for_brand_check.name}' has a brand. "
                            f"brand_id not set from partner."
                        )

        records = super().create(vals_list)

        # The onchange logic might also be triggered after creation if
        # partner_id is set,
        # but explicitly handling it here ensures it's
        # set during the initial create call
        # if possible. Re-triggering onchange or a direct write post-create is generally
        # less efficient if it can be handled in the initial vals.

        return records

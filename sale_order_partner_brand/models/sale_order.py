import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id")
    def _onchange_partner_id_set_brand(self):
        """
        Onchange method to set the brand_id on the Sales Order
        based on the selected customer's commercial entity brand,
        or the customer's own brand if the commercial entity has no brand.
        """
        brand_to_set = False  # Initialize brand_to_set at the beginning

        if self.partner_id:
            # Determine the partner whose brand should be checked:
            # 1. Commercial entity (parent company)
            # 2. The partner itself if no commercial entity
            #    or if commercial entity has no brand
            partner_for_brand_check = (
                self.partner_id.commercial_partner_id or self.partner_id
            )

            if (
                hasattr(partner_for_brand_check, "brand_id")
                and partner_for_brand_check.brand_id
            ):
                brand_to_set = partner_for_brand_check.brand_id
                _logger.debug(
                    f"SO (onchange {self.name or 'New'}): Partner "
                    f"'{self.partner_id.name}' selected. "
                    f"Using brand from commercial entity "
                    f"'{partner_for_brand_check.name}': '{brand_to_set.name}' "
                    f"(ID: {brand_to_set.id})."
                )
            elif hasattr(self.partner_id, "brand_id") and self.partner_id.brand_id:
                # Fallback to the direct partner's brand
                brand_to_set = self.partner_id.brand_id
                _logger.debug(
                    f"SO (onchange {self.name or 'New'}): Partner "
                    f"'{self.partner_id.name}' selected. "
                    f"Commercial entity '{partner_for_brand_check.name}' has no brand. "
                    f"Using brand from direct partner: '{brand_to_set.name}' "
                    f"(ID: {brand_to_set.id})."
                )
            else:
                # Partner and its commercial entity have no brand,
                # brand_to_set remains False
                _logger.debug(
                    f"SO (onchange {self.name or 'New'}): Partner "
                    f"'{self.partner_id.name}' selected. "
                    f"Neither partner nor its commercial entity "
                    f"'{partner_for_brand_check.name}' has a brand. Clearing brand."
                )
        else:
            # Partner is cleared, brand_to_set remains False
            _logger.debug(
                f"SO (onchange {self.name or 'New'}): Partner cleared. "
                f"Clearing brand on SO."
            )

        # Centralized assignment of brand_id
        if hasattr(self, "brand_id"):
            self.brand_id = brand_to_set  # Assign the determined brand_to_set
        else:
            # This case should ideally not happen if sale_brand is correctly installed
            # and the field is present on the model.
            # Log a warning if we intended to set a brand but the field is missing.
            if self.partner_id or brand_to_set:
                _logger.warning(
                    "Sales Order model does not appear to have a 'brand_id' field. "
                    "Is 'sale_brand' module installed and loaded correctly?"
                )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to ensure brand_id is set from partner_id's commercial entity
        (or partner itself) if provided during direct creation,
        and not already set in vals.
        """
        for vals in vals_list:
            # Only attempt to set brand_id if partner_id is provided
            # and brand_id is not already explicitly provided in vals
            if vals.get("partner_id") and "brand_id" not in vals:
                partner = self.env["res.partner"].browse(vals.get("partner_id"))
                if partner.exists():
                    # Determine the partner whose brand should be checked
                    partner_for_brand_check = partner.commercial_partner_id or partner
                    brand_to_set_on_create = False  # Initialize

                    if (
                        hasattr(partner_for_brand_check, "brand_id")
                        and partner_for_brand_check.brand_id
                    ):
                        brand_to_set_on_create = partner_for_brand_check.brand_id
                        _logger.debug(
                            f"Create SO: Partner '{partner.name}' provided. "
                            f"Using brand from commercial entity "
                            f"'{partner_for_brand_check.name}': "
                            f"'{brand_to_set_on_create.name}'."
                        )
                    elif hasattr(partner, "brand_id") and partner.brand_id:
                        # Fallback to the direct partner's brand
                        brand_to_set_on_create = partner.brand_id
                        _logger.debug(
                            f"Create SO: Partner '{partner.name}' provided. "
                            f"Commercial entity '{partner_for_brand_check.name}' "
                            f"has no brand. "
                            f"Using brand from direct partner: "
                            f"'{brand_to_set_on_create.name}'."
                        )

                    if brand_to_set_on_create and "brand_id" in self._fields:
                        vals["brand_id"] = brand_to_set_on_create.id
                        _logger.debug(
                            f"Setting brand_id to {brand_to_set_on_create.id} "
                            f"in creation vals."
                        )
                    elif not brand_to_set_on_create:
                        _logger.debug(
                            f"Create SO: Partner '{partner.name}' provided. "
                            f"Neither partner nor its commercial entity has a brand. "
                            f"brand_id not set from partner."
                        )
                    elif "brand_id" not in self._fields:
                        _logger.warning(
                            "Sales Order model does not have a 'brand_id' field "
                            "during create. "
                            "Is 'sale_brand' module installed?"
                        )

        records = super().create(vals_list)
        return records

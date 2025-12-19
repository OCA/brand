# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_analytic_distribution_arguments(self):
        """
        Add the brand inside the arguments
        """
        self.ensure_one()
        return {
            "product_id": self.product_id.id,
            "product_categ_id": self.product_id.categ_id.id,
            "partner_id": self.order_id.partner_id.id,
            "partner_category_id": self.order_id.partner_id.category_id.ids,
            "company_id": self.company_id.id,
            "brand_id": self.order_id.brand_id.id,
        }

    @api.depends("order_id.brand_id")
    def _compute_analytic_distribution(self):
        res = super()._compute_analytic_distribution()
        # This code improves Odoo method in sale/models/sale_order_line.py
        # by replacing the hardcoded dict by a method,
        # to be able to add parameters inside _get_distribution params.
        for line in self:
            if not line.display_type:
                distribution = line.env[
                    "account.analytic.distribution.model"
                ]._get_distribution(line._get_analytic_distribution_arguments())
                line.analytic_distribution = distribution or line.analytic_distribution
        return res

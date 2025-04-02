from odoo import fields, models


class ProductPricelistPrintBrand(models.TransientModel):
    _inherit = "product.pricelist.print"

    brand_id = fields.Many2one("res.brand")

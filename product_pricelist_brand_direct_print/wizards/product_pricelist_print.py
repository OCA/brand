from odoo import models


class ProductPricelistPrint(models.TransientModel):
    _name = "product.pricelist.print"
    _inherit = ["product.pricelist.print", "res.brand.mixin"]

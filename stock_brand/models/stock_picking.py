#  Copyright (C) 2019 Sunflower IT <sunflowerweb.nl>
#  License GNU Affero General Public License <http://www.gnu.org/licenses/>.

from odoo import fields, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "res.brand.mixin"]

    brand_id = fields.Many2one(
        help="Brand to use for this picking.",
    )

    def _is_brand_required(self):
        self.ensure_one()
        if self.picking_type_id.code == "internal":
            return False
        return super()._is_brand_required()

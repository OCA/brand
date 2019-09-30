#  Copyright (C) 2019 Sunflower IT <sunflowerweb.nl>
#  License GNU Affero General Public License <http://www.gnu.org/licenses/>.

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    brand_id = fields.Many2one(
        'res.brand', string='Brand',
        help="Brand to use for this picking")

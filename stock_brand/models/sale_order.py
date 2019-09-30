#  Copyright (C) 2019 Sunflower IT <sunflowerweb.nl>
#  License GNU Affero General Public License <http://www.gnu.org/licenses/>.

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        ret = super(SaleOrder, self).action_confirm()
        for order in self:
            order.picking_ids.write({'brand_id': order.brand_id.id})
        return ret

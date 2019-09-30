# -*- coding: utf-8 -*-
#  Copyright (C) 2019 Sunflower IT <sunflowerweb.nl>
#  License GNU Affero General Public License <http://www.gnu.org/licenses/>.

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    brand_id = fields.Many2one(
        'res.brand', string='Brand',
        help="Brand to use for this sale")


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def _action_confirm(self):
        ret = super(StockMove, self)._action_confirm()
        for this in self:
            if this.sale_line_id.order_id:
                this.picking_id.brand_id = this.sale_line_id.order_id.brand_id
        return ret
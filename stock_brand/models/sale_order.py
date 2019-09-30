# -*- coding: utf-8 -*-
#  Copyright (C) 2019 Sunflower IT <sunflowerweb.nl>
#  License GNU Affero General Public License <http://www.gnu.org/licenses/>.

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        ret = super(SaleOrder, self).action_confirm()
        for this in self:
            for picking in this.picking_ids:
                picking.brand_id = this.brand_id.id
        return ret
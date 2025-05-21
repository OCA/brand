#  Copyright (C) 2019 Sunflower IT <sunflowerweb.nl>
#  License GNU Affero General Public License <http://www.gnu.org/licenses/>.

{
    "name": "Stock Brand",
    "summary": "Manage brands on stock picking documents",
    "version": "16.0.1.0.0",
    "category": "Warehouse",
    "website": "https://github.com/OCA/brand",
    "author": "Sunflower IT, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "sale_brand",
        "sale_stock",
    ],
    "data": [
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "development_status": "Beta",
}

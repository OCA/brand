#  Copyright (C) 2019 Sunflower IT <sunflowerweb.nl>
#  License GNU Affero General Public License <http://www.gnu.org/licenses/>.

{
    "name": "Stock Brand",
    "summary": "Manage branded delivery orders",
    "version": "12.0.1.0.0",
    "category": "Stock Management",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "author": "Sunflower IT, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        'sale_stock',
    ],
    "data": [
        "views/sale_views.xml",
    ],
    "installable": True,
    "development_status": "Beta"
}

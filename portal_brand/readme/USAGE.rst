1. Configure Brand Logos: Ensure that you have configured brand logos in your system.  This usually involves setting a logo on the brand records within Odoo.

2. Access the Portal: When users access the Odoo portal, the header logo will dynamically change. If a brand logo is set, it will be displayed. If no brand logo is set, the default company logo will be shown.

This module does nothing in itself. It depends on other modules to have the brand_id available on the model.
e.g. `account_brand`, `sale_brand`.

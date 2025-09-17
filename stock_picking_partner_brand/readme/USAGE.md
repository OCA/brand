## Automatic Brand Setting
When you are on a Stock Picking form:

Selecting a Customer with a Brand:

If you select a customer in the "Customer" (partner_id) field, and that customer has a brand assigned to them (via the brand_id field on their contact record), the "Brand" field on the Stock picking will automatically be populated with the customer's brand.

Selecting a Customer without a Brand:

If you select a customer who does not have a brand assigned to them, the "Brand" field on the Stock  Picking will be automatically cleared (set to empty/None).

*Changing Customer*:

If you change the customer on an existing picking, the brand on the picking will update according to the newly selected customer's brand (or be cleared if the new customer has no brand).

Clearing Customer:

If you clear the "Customer" field on the stock picking (remove the selected customer), the "Brand" field on the stock picking will also be automatically cleared.

This behavior is triggered by an onchange mechanism on the partner_id field of the stock.picking model.

*Manual Override*
The automatic setting of the brand based on the customer is a default behavior. After the brand is automatically populated (or cleared), you can still manually change or set the brand on the Stock Picking directly if needed. The onchange mechanism only triggers when the partner_id field itself is modified.

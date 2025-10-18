This module enhances Odoo's email communication with branding
capabilities.

**Key Features:**

- **Comprehensive Email Branding:** Automatically applies branding to outgoing emails. This includes:  
  - Displaying the correct brand logo, derived from the linked partner's
    image.
  - Setting the sender's company details (website, address, phone
    number) according to the selected brand's information.

- **Website Contextualization:** Dynamically adjusts the base URL for
  links within emails to reflect the website associated with a selected
  brand.

- **Brand Selection in Email compose wizard:** Extends the standard
  "Compose Email" wizard with a 'Brand' selection field. This allows
  users to explicitly apply a brand to outgoing emails, particularly
  useful when the originating record isn't directly linked to a brand.

- **Dynamic Logo Delivery:** Includes a custom controller to serve the
  appropriate brand logo in emails based on the selected brand context.

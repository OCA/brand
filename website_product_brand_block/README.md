# Website Product Brand Block

This Odoo 18 module adds a dynamic brand block to the product detail page on the website. It displays the brand logo and name, styled with hover effects and linked to a filtered brand-specific product listing.

## ✨ Features

- Displays brand logo and name on product detail pages.
- Clickable block linking to `/shop/brands?brand=<brand_id>`.
- Tooltip with brand name for accessibility.
- CSS hover effect with scale and yellow tint.
- Fully modular and upgrade-safe.
- Internationalization-ready (i18n).

## 📦 Installation

1. Clone the repository into your Odoo addons directory:
   ```bash
   git clone https://github.com/yourusername/website_product_brand_block.git
   ```
2. Restart your Odoo server.
3. Activate developer mode.
4. Install the module from the Apps menu.

## 🛠️ Configuration

Ensure the `product_brand` module is installed and brands are assigned to products via the `product_brand_id` field.

## 🌐 Internationalization

All user-facing strings are in English and marked for translation using Odoo's `t-translation` attributes. You can translate them via the Odoo interface or export `.po` files.

## 🧩 Customization

You can adjust:

- Logo size via CSS (`max-height`, `max-width`)
- Blend mode (`mix-blend-mode: color`, `overlay`, etc.)
- Tooltip text
- Link target (`_blank`, internal routing)
- Positioning via XPath


## 🧑‍💻 Author

Developed by [Fernando](https://github.com/fernandogiacomino) with Copilot
Modular, scalable, and OWL-ready.

## 📄 License

This module is released under the MIT License.
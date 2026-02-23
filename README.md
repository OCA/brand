
[![Runboat](https://img.shields.io/badge/runboat-Try%20me-875A7B.png)](https://runboat.odoo-community.org/builds?repo=OCA/brand&target_branch=18.0)
[![Pre-commit Status](https://github.com/OCA/brand/actions/workflows/pre-commit.yml/badge.svg?branch=18.0)](https://github.com/OCA/brand/actions/workflows/pre-commit.yml?query=branch%3A18.0)
[![Build Status](https://github.com/OCA/brand/actions/workflows/test.yml/badge.svg?branch=18.0)](https://github.com/OCA/brand/actions/workflows/test.yml?query=branch%3A18.0)
[![codecov](https://codecov.io/gh/OCA/brand/branch/18.0/graph/badge.svg)](https://codecov.io/gh/OCA/brand)
[![Translation Status](https://translation.odoo-community.org/widgets/brand-18-0/-/svg-badge.svg)](https://translation.odoo-community.org/engage/brand-18-0/?utm_source=widget)

<!-- /!\ do not modify above this line -->

# brand

brand

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[account_brand](account_brand/) | 18.0.1.0.1 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Send branded invoices and refunds
[account_invoice_bank_brand](account_invoice_bank_brand/) | 18.0.1.0.0 |  | Enables the automatic selection of the partner'sbank account on invoices based on the brand.
[account_payment_mode_brand](account_payment_mode_brand/) | 18.0.1.0.0 |  | This addon define allowed payment mode per brand
[analytic_brand](analytic_brand/) | 18.0.1.1.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This addon associate an analytic account to a brand that will be used as a default value where the brand is used if the analytic accounting is activated
[brand](brand/) | 18.0.1.0.2 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This is a base addon for brand modules. It adds the brand object and its menu and define an abstract model to be inherited from branded objects
[brand_external_report_layout](brand_external_report_layout/) | 18.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows you to have a different layout by brand for your external reports.
[contract_brand](contract_brand/) | 18.0.1.0.0 | <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | This module allows you to manage branded contracts. It adds a brand field on the contract and propagate the value on the invoices.
[contract_forecast_brand](contract_forecast_brand/) | 18.0.1.0.0 |  | This addon add brand field for contract forecast
[contract_payment_mode_brand](contract_payment_mode_brand/) | 18.0.1.0.0 |  | This addon limits payment mode selection in contract to the brand's allowed.
[mail_brand](mail_brand/) | 18.0.1.0.0 | <a href='https://github.com/switch87'><img src='https://github.com/switch87.png' width='32' height='32' style='border-radius:50%;' alt='switch87'/></a> <a href='https://github.com/bosd'><img src='https://github.com/bosd.png' width='32' height='32' style='border-radius:50%;' alt='bosd'/></a> | If a model has a brand defined to it, emails send from this model will be branded accordingly.
[partner_brand](partner_brand/) | 18.0.1.0.2 | <a href='https://github.com/bealdav'><img src='https://github.com/bealdav.png' width='32' height='32' style='border-radius:50%;' alt='bealdav'/></a> | Define registered mark in partners according to brand settings
[product_brand](product_brand/) | 18.0.1.1.0 |  | Product Brand Manager
[product_brand_mrp](product_brand_mrp/) | 18.0.1.0.0 |  | This module allows to work with product_brand in MRP.
[product_brand_purchase](product_brand_purchase/) | 18.0.1.0.0 |  | This module allows to work with product_brand in purchase reports.
[product_brand_stock](product_brand_stock/) | 18.0.1.0.0 |  | This module allows to work with product_brand in Stock.
[product_brand_stock_account](product_brand_stock_account/) | 18.0.1.0.0 |  | This module allows to work with product_brand in Stock Account.
[product_brand_tag](product_brand_tag/) | 18.0.1.0.0 |  | Add tags to product brand
[product_contract_brand](product_contract_brand/) | 18.0.1.0.0 |  | This addon propagate the brand from sale order to contract
[sale_brand](sale_brand/) | 18.0.1.0.0 | <a href='https://github.com/osi-scampbell'><img src='https://github.com/osi-scampbell.png' width='32' height='32' style='border-radius:50%;' alt='osi-scampbell'/></a> <a href='https://github.com/sbejaoui'><img src='https://github.com/sbejaoui.png' width='32' height='32' style='border-radius:50%;' alt='sbejaoui'/></a> | Send branded sales orders
[sale_payment_mode_brand](sale_payment_mode_brand/) | 18.0.1.0.0 |  | This addon limit payment mode selection on sale order to the brand allowed payment modes.
[stock_brand](stock_brand/) | 18.0.1.0.0 |  | Manage brands on stock picking documents
[stock_picking_partner_brand](stock_picking_partner_brand/) | 18.0.1.0.0 | <a href='https://github.com/bosd'><img src='https://github.com/bosd.png' width='32' height='32' style='border-radius:50%;' alt='bosd'/></a> | Automatically sets the brand on a Stock Picking based on the selected partner's brand.

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
OCA, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit
organization whose mission is to support the collaborative development of Odoo features
and promote its widespread use.

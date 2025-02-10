To use this module, you need to:

Define a pdf watermark on brand.
1.  go to settings --\> User & Companies --\> Brands
2.  create or edit an brand
3.  upload an pdf watermark. Note that resolutions and
    size must match, otherwise you'll have funny results

To use the Brand watermark, on for example your invoices with the `account_brand` module you need to:

1.  go to your report settings --\> Technical --\> Reports
    (e.g. `account.report_invoice`)
2.  Under Advanced Properties, Check the box "Use Brand Watermark".
3.  Create a report e.g. an invoice, Set the brand and generate the report.
    The brand watermark is added there.

If no brand information is available. No watermark is added.
It is possible to stack the pdf watermarks. E.g. use the "Company watermark" and "Brand Watermark" on top of each other.

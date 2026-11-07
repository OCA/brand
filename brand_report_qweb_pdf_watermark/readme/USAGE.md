Define a pdf watermark on a brand:

1.  Go to Settings → Users & Companies → Brands.
2.  Create or edit a brand.
3.  Upload a pdf watermark. Note that resolution and size must match the
    report paper format, otherwise you'll get funny results.

To use the brand watermark on, for example, invoices with the
`account_brand` module:

1.  Go to Settings → Technical → Reports (e.g. `account.report_invoice`).
2.  Under Advanced Properties, check the box "Use Brand Watermark".
3.  Print an invoice that has a brand set. The brand watermark is added.

If the printed record has no brand, or the brand has no watermark, no brand
watermark is added. When several records are printed at once, the brand of
the first record is used.

The brand watermark can be combined with the watermarks of
`report_qweb_pdf_watermark` (e.g. "Use Company Watermark"). The brand
watermark is the bottom layer, the other watermark is stacked on top of it.
For the brand watermark to remain visible, the watermark on top must have a
transparent background.

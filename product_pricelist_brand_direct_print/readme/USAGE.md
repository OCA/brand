
To use this module, you need to:

1.  **Access the Pricelist Printing Wizard:**
    * Navigate to the area in Odoo where you typically generate product pricelists (e.g., Sales > Products > Print Price List).
    * Initiate the process to print a pricelist. This will usually open a wizard or dialog provided by the `product_pricelist_direct_print` module.

2.  **Select a Brand (Optional):**
    * In the pricelist printing wizard, you will now see a new field labeled "Brand".
    * If you want to include brand information in the generated PDF, select the desired brand from the dropdown menu.
    * If you leave this field empty, the report will be generated using the standard layout.

3.  **Configure Other Print Options:**
    * Set any other options available in the wizard, such as which information to include (e.g., cost price, Sales Description), which products to include, etc.

4.  **Generate the PDF:**
    * Click the "Print" button to create the pricelist report.

## Output

* **With a Selected Brand:** If you selected a brand, the generated PDF will include brand-specific information, such as the brand's logo, name, and any other details configured in the `brand_external_report_layout` module.
* **Without a Selected Brand:** If you did not select a brand, the PDF will be generated using the standard layout defined in the company settings.

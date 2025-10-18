**1. Defining Brands:**

- Navigate to **Contacts \> Brands**.

- Create new brand records. For each brand, you can:  
  - **Partner:** Link the brand to an existing partner (company). The
    logo displayed in emails will be derived from the image of this
    partner. Ensure the partner has a logo uploaded (visible in the
    contact form).
  - **Website:** Optionally specify a website URL associated with the
    brand. This URL may be used for links in emails.

**2. Automatic Email Branding (Based on Originating Record):**

- When sending emails from records that have a `brand_id` field
  populated (e.g., Sales Orders, Invoices, or other relevant models),
  the module will automatically attempt to use the branding associated
  with that record's brand.
- The email will display the logo of the linked brand, and any company
  details (website, address, phone number) in the email footer should
  correspond to the brand's partner information.

**3. Manual Brand Selection (Using the Compose Email Wizard):**

- When composing a new email (e.g., via the "Send message" button in the
  chatter or through other email actions), a **Brand** field will be
  available in the "Compose Email" wizard. ( The brand field is only
  available in the full view of the compose wizard. )

- Usefull if the originating record does not have a `brand_id` set, or
  if you want to use a different brand for this specific email:

  > 1.  Open the "Compose Email" wizard.
  > 2.  In the wizard form, select the desired brand from the **Brand**
  >     dropdown field.
  > 3.  Compose your email content as usual.
  > 4.  Click **Send**.

- The email sent will then use the logo and company details associated
  with the brand you selected in the wizard.

**4. Website Links in Emails:**

- If a website is defined for the selected brand, the module may use
  this website URL for any relevant links included in the email.

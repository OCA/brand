This module introduces the following features:

- It introduces the brand to mail.
- We have the possibility to set an outgoing mail for each brand.
- We have the possibility to set the brand for each mail alias.
- We have the possibility to set the brand on each user for mails if brand_id does not exist on record.
- If a brand is set in a mail alias it sets the domain according its brand.
- We have the possibility to set the brand for each mail template.
- If we sent a mail (ex. via sale order) we can only select the templates of
  the same model where the brand is not set or of the same brand.
- If we sent a mail within a record it sets the sender_email_address (alias and
  domain) and reply_to according its brand.

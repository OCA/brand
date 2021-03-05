#. Create an Outgoing Mail Server.
#. Use a current Brand or create a new one.
#. Set values into the new fields 'Catchall alias', 'Catchall domain',
   'Outgoing Mail Server').
#. Assignment of a brand to a mail alias. Then it takes the domain set in the brand
   as domain for this mail alias. If no brand set, it takes the one from system
   parameters. If the set brand has no 'Catchall domain' set, it stays
   empty.
#. Assignment of a brand to a mail template. If we sent a mail (ex. via sale
   order) we can only select the templates of the same model where the brand is
   not set or of the same brand. If we sent a mail within a record it sets the
   sender_email_address (alias and domain) and reply_to according its brand.

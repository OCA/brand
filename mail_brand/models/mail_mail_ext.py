# Copyright 2021 Yves Goldberg
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from email.utils import formataddr

from odoo import models


class MailMailExt(models.Model):
    _inherit = "mail.mail"

    def create(self, vals_list):
        mails = super(MailMailExt, self).create(vals_list)

        for mail in mails:
            brand = False
            if mail.mail_message_id.model and mail.mail_message_id.res_id:
                model = mail.mail_message_id.model
                res_id = mail.mail_message_id.res_id
                record = self.env[model].browse(res_id)
                if getattr(record, "brand_id", False):
                    brand = record.brand_id
            if not brand and self.env.context.get("uid", False):
                user = self.env["res.users"].browse(self.env.context.get("uid"))
                brand = user.brand_for_mails_id

            if brand and brand.catchall_alias and brand.catchall_domain:
                sender_email_address = (
                    brand.catchall_alias + "@" + brand.catchall_domain
                )
                email_name = brand.partner_id.name
                mail.email_from = formataddr((email_name, sender_email_address))
                mail.reply_to = mail.email_from

                if brand.outgoing_mail_server_id:
                    mail.mail_server_id = brand.outgoing_mail_server_id.id

        return mails

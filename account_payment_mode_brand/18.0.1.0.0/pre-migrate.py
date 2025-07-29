# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    cr.execute(
        """
        DELETE FROM ir_ui_view
        WHERE id IN (
        SELECT res_id
        FROM ir_model_data
        WHERE name='account_invoice_form_view'
        AND module='account_payment_mode_brand'
        AND model='ir.ui.view';
        )
        """
    )
    cr.execute(
        """
        DELETE FROM ir_model_data
        WHERE name='account_invoice_form_view'
        AND module='account_payment_mode_brand'
        AND model='ir.ui.view';
        """
    )

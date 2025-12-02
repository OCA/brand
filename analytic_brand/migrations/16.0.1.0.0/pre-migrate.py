# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE res_brand
        ADD analytic_distribution jsonb;
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_brand
        SET analytic_distribution = jsonb_build_object(analytic_account_id, 100.0)
        WHERE analytic_account_id IS NOT NULL;
        """,
    )

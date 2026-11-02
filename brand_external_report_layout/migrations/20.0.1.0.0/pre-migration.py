# Copyright 2026 Juliano Henriquez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    cr.execute(
        "UPDATE res_brand SET font = %s WHERE font = %s",
        ("Noto_Sans_Mono", "Fira_Mono"),
    )

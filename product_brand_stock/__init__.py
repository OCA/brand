# Copyright 2023 Francesco Apruzzese <cescoap@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import sql

from . import models


def pre_init_hook(cr):
    to_init_tables = (
        "stock_move",
        "stock_move_line",
        "stock_quant",
    )
    for to_init_table in to_init_tables:
        query_alter = sql.SQL(
            "ALTER TABLE {} ADD COLUMN IF NOT EXISTS product_brand_id integer"
        ).format(sql.Identifier(to_init_table))
        query_update = sql.SQL(
            "UPDATE {} x SET product_brand_id=t.product_brand_id "
            "FROM product_product p "
            "INNER JOIN product_template t ON t.id = p.product_tmpl_id "
            "WHERE x.product_id=p.id"
        ).format(sql.Identifier(to_init_table))
        cr.execute(query_alter)
        cr.execute(query_update)

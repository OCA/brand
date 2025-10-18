# Copyright (C) 2022 Snakebyte
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import functools
import io

import odoo
from odoo import http
from odoo.modules import get_resource_path
from odoo.tools.mimetypes import guess_mimetype

from odoo.addons.web.controllers.main import Binary


class BrandBinary(Binary):
    @http.route()
    def company_logo(self, dbname=None, **kw):
        response = False
        imgname = "logo"
        imgext = ".png"
        uid = None
        placeholder = functools.partial(get_resource_path, "web", "static", "img")
        if http.request.session.db:
            dbname = http.request.session.db
            uid = http.request.session.uid
        elif dbname is None:
            dbname = http.db_monodb()
        if not uid:
            uid = odoo.SUPERUSER_ID
        if not dbname:
            response = http.send_file(placeholder(imgname + imgext))
        else:
            try:
                has_brand = int(kw["bstyle"]) if kw and kw.get("bstyle") else False
                if has_brand:
                    registry = odoo.modules.registry.Registry(dbname)
                    with registry.cursor() as cr:
                        brand = int(kw["company"])
                        if brand:
                            cr.execute(
                                """
                                SELECT logo_web, write_date
                                FROM res_brand
                                WHERE id = %s
                                """,
                                (brand,),
                            )
                            row = cr.fetchone()
                            if row and row[0]:
                                image_base64 = base64.b64decode(row[0])
                                image_data = io.BytesIO(image_base64)
                                mimetype = guess_mimetype(
                                    image_base64, default="image/png"
                                )
                                imgext = "." + mimetype.split("/")[1]
                                if imgext == ".svg+xml":
                                    imgext = ".svg"
                                response = http.send_file(
                                    image_data,
                                    filename=imgname + imgext,
                                    mimetype=mimetype,
                                    mtime=row[1],
                                )
            except Exception:
                response = http.send_file(placeholder(imgname + imgext))
        return response or super().company_logo(dbname, **kw)

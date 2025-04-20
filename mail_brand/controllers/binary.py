# Copyright (C) 2022 Snakebyte
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import io

import odoo
from odoo import http
from odoo.http import Response, request  # Import Response
from odoo.tools.mimetypes import guess_mimetype

from odoo.addons.web.controllers.binary import Binary

try:
    from werkzeug.utils import send_file
except ImportError:
    from odoo.tools._vendor.send_file import send_file

from odoo.tools import file_path


class BrandBinary(Binary):
    @http.route(
        [
            "/web/binary/company_logo",
            "/logo",
            "/logo.png",
        ],
        type="http",
        auth="none",
        cors="*",
    )
    def company_logo(self, dbname=None, **kw):
        response = False
        imgname = "logo"
        imgext = ".png"
        dbname = request.db

        if not dbname:
            response = http.Stream.from_path(
                file_path("web/static/img/logo.png")
            ).get_response()
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
                                response = send_file(
                                    image_data,
                                    request.httprequest.environ,
                                    download_name=imgname + imgext,
                                    mimetype=mimetype,
                                    last_modified=row[1],
                                    response_class=Response,
                                )

            except Exception:
                response = http.Stream.from_path(
                    file_path(f"web/static/img/{imgname}{imgext}")
                ).get_response()
        return response or super().company_logo(dbname, **kw)

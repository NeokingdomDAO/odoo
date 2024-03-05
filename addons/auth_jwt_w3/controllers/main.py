import json
from odoo.http import Controller, Response, request, route

class JWTW3Controller(Controller):
    @route(
        "/auth_jwt_w3",
        type="http",
        auth="none",
        csrf=False,
        cors="*",
        save_session=False,
        methods=["GET"],
    )
    def get_w3_signing_token(self):
        data = {
            'signing_token': request.env['auth.jwt.w3.validator'].get_signing_token(),
        }
        return Response(json.dumps(data), content_type="application/json", status=200)

import base64
import datetime
import json
import jwt
import uuid
from datetime import timedelta
from hexbytes import HexBytes
from web3.auto import w3
from eth_account.messages import encode_defunct
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class AuthJWTW3Validator(models.AbstractModel):
    _name = 'auth.jwt.w3.validator'
    _description = 'Auth JWT W3 Validator'

    @api.model
    def get_signing_token(self):
        IrConfigParameter = self.env['ir.config_parameter'].sudo()
        server_secret = IrConfigParameter.get_param('auth.jwt.w3.server_secret')
        try:
            valid_seconds = int(IrConfigParameter.get_param('auth.jwt.w3.valid_seconds', 600))
            assert server_secret
        except:
            return False
        message_template = IrConfigParameter.get_param('auth.jwt.w3.message_template.prefix', '')
        message_template += ' #{}'.format(uuid.uuid4().hex)
        payload = {
            "exp": fields.Datetime.now() + timedelta(seconds=valid_seconds),
            "message": message_template.format(uuid.uuid4().hex),
        }
        return jwt.encode(payload, server_secret, algorithm="HS256")

    @api.model
    def is_signing_token_valid(self, encoded_authentication):
        try:
            authentication = eval(base64.b64decode(encoded_authentication).decode())
            IrConfigParameter = self.env['ir.config_parameter'].sudo()
            server_secret = IrConfigParameter.get_param('auth.jwt.w3.server_secret') 
            payload = jwt.decode(authentication['signing_token'], server_secret, algorithms=["HS256"])
            message = encode_defunct(text=payload["message"])
            signer = w3.eth.account.recover_message(message, signature=authentication['signature'])
            return self.env.user.ethereum_address == signer.lower()
        except Exception as e:
            _logger.error(str(e))
            _logger.error('Wallet Authentication failed!')
            return False

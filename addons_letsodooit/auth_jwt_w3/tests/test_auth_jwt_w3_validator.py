import base64
import json
import jwt
from datetime import timedelta
from web3.auto import w3
from eth_account.messages import encode_defunct
from odoo import fields
from odoo.tests import common

import logging
_logger = logging.getLogger(__name__)

class TestAuthJWTW3Validator(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.server_secret = 'SeverSecret'
        self.env['ir.config_parameter'].set_param('auth.jwt.w3.server_secret', self.server_secret)
        self.user_id = self.env['res.users'].create({
            'login': 'RandomUser',
            'name': 'Random'
        })

    def test_get_signing_token_no_secret(self):
        self.env['ir.config_parameter'].set_param('auth.jwt.w3.server_secret', None)
        token = self.env['auth.jwt.w3.validator'].get_signing_token()
        self.assertFalse(token)

    def test_get_signing_token_set_secret(self):
        token = self.env['auth.jwt.w3.validator'].get_signing_token()
        self.assertTrue(token)
        payload = jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})
        self.assertTrue(payload['message'])
        self.assertTrue(payload['exp'])

    def test_message_template_prefix(self):
        message_template_prefix = 'Some Message Template'
        self.env['ir.config_parameter'].set_param('auth.jwt.w3.message_template.prefix', message_template_prefix)
        token = self.env['auth.jwt.w3.validator'].get_signing_token()
        payload = jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})
        self.assertIn(message_template_prefix, payload['message'])

    def test_jwt_expiration_default(self):
        default_expiration_seconds = 600
        before_generation_plus_600_seconds = fields.Datetime.now() + timedelta(seconds=default_expiration_seconds)
        token = self.env['auth.jwt.w3.validator'].get_signing_token()
        payload = jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})
        after_generation_plus_600_seconds = fields.Datetime.now() + timedelta(seconds=default_expiration_seconds)
        self.assertLessEqual(before_generation_plus_600_seconds.timestamp(), payload['exp'])
        self.assertGreaterEqual(after_generation_plus_600_seconds.timestamp(), payload['exp'])

    def test_jwt_expiration_set(self):
        expiration_seconds = 1600
        self.env['ir.config_parameter'].set_param('auth.jwt.w3.valid_seconds', expiration_seconds)
        before_generation_plus_1600_seconds = fields.Datetime.now() + timedelta(seconds=expiration_seconds)
        token = self.env['auth.jwt.w3.validator'].get_signing_token()
        payload = jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})
        after_generation_plus_1600_seconds = fields.Datetime.now() + timedelta(seconds=expiration_seconds)
        self.assertLessEqual(before_generation_plus_1600_seconds.timestamp(), payload['exp'])
        self.assertGreaterEqual(after_generation_plus_1600_seconds.timestamp(), payload['exp'])

    def test_jwt_expiration_set(self):
        expiration_seconds = '1600x'
        self.env['ir.config_parameter'].set_param('auth.jwt.w3.valid_seconds', expiration_seconds)
        token = self.env['auth.jwt.w3.validator'].get_signing_token()
        self.assertFalse(token)

    def test_validation(self):
        wallet = w3.eth.account.create()
        self.user_id.write({'ethereum_address': wallet.address})
        token = self.env['auth.jwt.w3.validator'].get_signing_token()
        payload = jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})
        message = encode_defunct(text=payload["message"])
        signed_message = w3.eth.account.sign_message(message, private_key=wallet.privateKey)
        post_data = {'signing_token': token, 'signature': signed_message.signature}
        post_data = base64.urlsafe_b64encode(str(post_data).encode())
        result = self.env['auth.jwt.w3.validator'].with_user(self.user_id).is_signing_token_valid(post_data)
        self.assertTrue(result)

    def test_validation_wrong_secret(self):
        wallet = w3.eth.account.create()
        self.user_id.write({'ethereum_address': wallet.address})
        token = self.env['auth.jwt.w3.validator'].get_signing_token()
        self.env['ir.config_parameter'].set_param('auth.jwt.w3.server_secret', 'WrongSecret')
        payload = jwt.decode(token, algorithms=["HS256"], options={"verify_signature": False})
        message = encode_defunct(text=payload["message"])
        signed_message = w3.eth.account.sign_message(message, private_key=wallet.privateKey)
        post_data = {'signing_token': token, 'signature': signed_message.signature}
        post_data = base64.urlsafe_b64encode(str(post_data).encode())
        result = self.env['auth.jwt.w3.validator'].with_user(self.user_id).is_signing_token_valid(post_data)
        self.assertFalse(result)

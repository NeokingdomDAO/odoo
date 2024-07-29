from odoo import http
from odoo.http import request
from eth_account.messages import encode_defunct
from eth_account import Account

class MetaMaskLogin(http.Controller):

    @http.route('/metamask/login', type='json', auth='public', csrf=False)
    def metamask_login(self, wallet_address, signature, message):
        # Verify the signature
        message_encoded = encode_defunct(text=message)
        recovered_address = Account.recover_message(message_encoded, signature=signature)

        if recovered_address.lower() == wallet_address.lower():  # ensure case-insensitive comparison
            user = request.env['res.users'].sudo().search([('ethereum_address', '=', wallet_address)], limit=1)
            if user:
                request.session.authenticate(request.env.cr.dbname, user.login, 'admin')
                return {'success': True}
            else:
                return {'success': False, 'message': 'Wallet address not associated with any account.'}
        else:
            return {'success': False, 'message': 'Signature verification failed.'}

from odoo.tests import common

class TestWalletDisablePasswordLogin(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.user_id = self.env['res.users'].create({
            'login': 'TestLogin',
            'name': 'TestUser',
            'email': 'email@test.com',
        })

    def test_disable_password_after_wallet_login(self):
        self.assertFalse(self.user_id.disable_password_login)
        self.user_id.write({'ethereum_address': 'SomeAddress'})
        self.assertTrue(self.user_id.disable_password_login)

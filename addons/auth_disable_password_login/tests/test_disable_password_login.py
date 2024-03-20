from odoo.tests import common 
from odoo.exceptions import AccessDenied, UserError

class TestDisablePasswordLogin(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.user_id = self.env['res.users'].create({
            'login': 'TestLogin',
            'name': 'TestUser',
            'email': 'email@test.com',
            'new_password': 'passwd'
        })

    def test_default_user_value(self):
        self.assertFalse(self.user_id.disable_password_login)

    def test_password_reset_when_disabled(self):
        self.user_id.write({'disable_password_login': True})
        self.assertFalse(self.user_id.password)
        self.assertFalse(self.user_id.new_password)

    def test_password_disabled_create(self):
        with self.assertRaises(UserError):
            self.user_id = self.env['res.users'].create({
                'login': 'TestLogin2',
                'name': 'TestUser2',
                'email': 'email2@test.com',
                'new_password': 'Password',
                'disable_password_login': True
            })

    def test_password_disabled_raise_exception(self):
        self.user_id.write({'disable_password_login': True})
        with self.assertRaises(AccessDenied):
            self.env['res.users'].with_user(self.user_id)._check_credentials('passwd', {'interactive': None})

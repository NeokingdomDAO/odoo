def migrate(cr, version):
    cr.execute(""" UPDATE res_users SET ethereum_address = LOWER(ethereum_address) """)

from odoo import api, models


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def web_search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, count_limit=None):
        # if the read is coming from web_search_read, then we should not create a history record, because it can
        # read the kanban view by column and the len == 1 condition is not filtering that
        _self = self.with_context({'from_web_search_read': True})
        return super(Base, _self).web_search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order, count_limit=count_limit)
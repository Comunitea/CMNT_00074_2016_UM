# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    @api.depends('sale_order_ids')
    def _get_order_str(self):
        order_names = []
        for l in self.sale_order_ids:
            if l.name not in order_names:
                order_names.append(l.name)
        self.orden_origin = ''
        if order_names:
            self.order_origin = ','.join(order_names)

    order_origin = fields.Char('Order origin', compute='_get_order_str')

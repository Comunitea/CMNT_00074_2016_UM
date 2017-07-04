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

    @api.multi
    def _from_web_site(self):
        for inv in self:
            if inv.sale_order_ids and inv.sale_order_ids[0].website_sale:
                inv.from_website = True

    order_origin = fields.Char('Order origin', compute='_get_order_str')
    from_website = fields.Boolean('From website', compute='_from_web_site')

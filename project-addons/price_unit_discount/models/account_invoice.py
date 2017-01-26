# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_id',
                 'product_id', 'invoice_id.partner_id',
                 'invoice_id.currency_id')
    def _compute_net(self):
        if self.discount:
            self.net_price_unit = \
                self.price_unit * (1 - (self.discount or 0.0) / 100.0)

            if self.invoice_id:
                self.net_price_unit = \
                    self.invoice_id.currency_id.round(self.net_price_unit)

    net_price_unit = fields.Float(string='Price unit net',
                                  digits=dp.get_precision('Account'),
                                  store=True,
                                  readonly=True, compute='_compute_net')

# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.one
    @api.depends('discount1', 'discount2', 'discount3', 'discount4')
    def _compute_discount(self):
        self.discount = self.discount1 + self.discount2 + self.discount3\
            + self.discount4

    discount = fields.Float(string='Discount (%)',
                            digits=dp.get_precision('Discount'),
                            default=0.0,
                            compute='_compute_discount',
                            store=True)
    discount1 = fields.Float('Discount 1')
    discount2 = fields.Float('Discount 2')
    discount3 = fields.Float('Discount 3')
    discount4 = fields.Float('Discount 4')

# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    promo_discount1 = fields.Many2one('promos.rules',
                                      string='Comercial Discount 1',
                                      readonly=False, copy=False)
    promo_discount2 = fields.Many2one('promos.rules',
                                      string='Comercial Discount 2',
                                      readonly=False, copy=False)
    promo_discount3 = fields.Many2one('promos.rules',
                                      string='Comercial Discount 3',
                                      readonly=False, copy=False)
    promo_discount4 = fields.Many2one('promos.rules',
                                      string='Comercial Discount 4',
                                      readonly=False, copy=False)


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
    discount1 = fields.Float('Disc. 1')
    discount2 = fields.Float('Disc. 2')
    discount3 = fields.Float('Disc. 3')
    discount4 = fields.Float('Disc. 4')

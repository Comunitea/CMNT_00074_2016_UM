# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    promo_discount1 = fields.Many2one('promos.rules',
                                      string='Promotion in Discount 1',
                                      readonly=True, copy=False)
    promo_discount2 = fields.Many2one('promos.rules',
                                      string='Promotion in Discount 2',
                                      readonly=True, copy=False)
    promo_discount3 = fields.Many2one('promos.rules',
                                      string='Promotion in Discount 3',
                                      readonly=True, copy=False)
    promo_discount4 = fields.Many2one('promos.rules',
                                      string='Promotion in Discount 4',
                                      readonly=True, copy=False)

    @api.multi
    def get_free_discount_field(self, promo):
        self.ensure_one()
        res = ''
        if promo.id == self.promo_discount1 or not self.promo_discount1:
            res = 'discount1'
        elif promo.id == self.promo_discount2 or not self.promo_discount2:
            res = 'discount2'
        elif promo.id == self.promo_discount3 or not self.promo_discount3:
            res = 'discount3'
        elif promo.id == self.promo_discount4 or not self.promo_discount4:
            res = 'discount4'
        return res

    @api.model
    def clear_existing_promotion_lines(self, order_id):
        res = super(SaleOrder, self).clear_existing_promotion_lines(order_id)
        order = self.browse(order_id)
        order.write({'promo_discount1': False,
                     'promo_discount2': False,
                     'promo_discount3': False,
                     'promo_discount4': False})
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

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
    discount1 = fields.Float('Disc. 1', copy=False)
    discount2 = fields.Float('Disc. 2', copy=False)
    discount3 = fields.Float('Disc. 3', copy=False)
    discount4 = fields.Float('Disc. 4', copy=False)

    @api.model
    def _prepare_order_line_invoice_line(self, line, account_id=False):
        """
        No Facturar el servicio punto verde, se hará al crear la factura el
        cálculo de nuevo
        """
        res = super(SaleOrderLine, self).\
            _prepare_order_line_invoice_line(line, account_id=False)
        res.update({
            'discount1': line.discount1,
            'discount2': line.discount2,
            'discount3': line.discount3,
            'discount4': line.discount4,
        })
        return res

# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import SUPERUSER_ID
from openerp import models, fields


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    coupon_discount_line = fields.Boolean()


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    coupons = fields.Many2many(
        'gift.coupon',
        'coupon_history',
        'sale_id',
        'coupon_id',
        'Coupons used')

    def _cart_update(self, cr, uid, ids, product_id=None, line_id=None,
                     add_qty=0, set_qty=0, context=None, **kwargs):
        """ Add or set product quantity, add_qty can be negative """
        sol = self.pool.get('sale.order.line')
        allow_update = True
        for so in self.browse(cr, uid, ids, context=context):
            if line_id is not False:
                line_ids = so._cart_find_product_line(
                    product_id, line_id, context=context, **kwargs)
                if line_ids:
                    line = sol.browse(
                        cr, SUPERUSER_ID, line_ids[0], context=context)
                    if line.coupon_discount_line:
                        allow_update = False
        if allow_update:
            return super(SaleOrder, self)._cart_update(
                cr, uid, ids, product_id, line_id, add_qty, set_qty,
                context, **kwargs)
        else:
            return {'line_id': line_id, 'quantity': line.product_uom_qty}

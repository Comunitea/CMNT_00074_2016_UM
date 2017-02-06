# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    website_sale = fields.Boolean('Website sale',
                                  related='partner_id.website_partner', store=True)

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0,
                     set_qty=0, **kwargs):
        total = 0
        orig_qty = 0
        new_line = True
        for line in self.order_line:
            if not line.product_id or line.product_id.type == 'service':
                continue
            if line.id == line_id:
                new_line = False
                orig_qty = line.product_uom_qty
                total += set_qty or line.product_uom_qty + (add_qty or 0)
            else:
                total += line.product_uom_qty
        if new_line:
            total += set_qty or add_qty
        if total > 6:
            res = {'line_id': line_id, 'quantity': orig_qty}
        else:
            res = super(SaleOrder, self)._cart_update(product_id, line_id,
                                                      add_qty, set_qty,
                                                      **kwargs)
        return res


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    original_price_unit = fields.Float(compute='_get_original_price_unit')

    @api.multi
    def _get_original_price_unit(self):
        for line in self:
            pricelist = line.order_id.partner_id.property_product_pricelist
            line.original_price_unit = pricelist.with_context(
                date=line.order_id.date_order,
                uom=line.product_uom.id).price_get(
                line.product_id.id, line.product_uom_qty,
                line.order_id.partner_id)[pricelist.id]

# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def create_green_point_line(self):
        for order in self:
            prod = self.env.ref('sale_line_green_point.product_green_point')
            # Delete green point lines to recalculate
            green_lines = order.order_line.filtered(lambda l:
                                                    l.product_id.id == prod.id)
            green_lines.unlink()

            # Get the qty of green line products
            qty = 0.0
            for line in order.order_line.filtered('product_id.green_point'):
                qty += line.product_uom_qty
            if qty:
                vals = {
                    'order_id': order.id,
                    'product_id': prod.id,
                    'name': _('Green Point contribution'),
                    'product_uom_qty': qty,
                    'price_unit': prod.lst_price,
                    'product_uom': prod.uom_id.id,
                    'tax_id': [(6, 0, [x.id for x in prod.taxes_id])]
                }
                self.env['sale.order.line'].create(vals)
        return

    @api.multi
    def write(self, vals):
        # Recalculate green point qty if order lines modified
        res = super(SaleOrder, self).write(vals)
        if 'order_line' in vals:
            self.create_green_point_line()
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        res.create_green_point_line()
        return res


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def invoice_line_create(self):
        """
        No Facturar el servicio punto verde, se hará al crear la factura el
        cálculo de nuevo
        """
        lines_record = self.env['sale.order.line']
        prod = self.env.ref('sale_line_green_point.product_green_point')
        for l in self:
            if l.product_id and l.product_id.id == prod.id:
                continue
            lines_record += l
        res = super(SaleOrderLine, lines_record).invoice_line_create()
        return res

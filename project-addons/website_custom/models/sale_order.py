# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    website_sale = fields.Boolean('Website sale', related='partner_id.website_partner')

    @api.multi
    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        import ipdb; ipdb.set_trace()
        quantity = add_qty or set_qty
        total = quantity
        orig_qty = 0
        for line in self.order_line:
            if line.id == line_id:
                orig_qty = line.product_uom_qty
            total += line.product_uom_qty
        if total > 6:
            res = {'line_id': line_id, 'quantity': orig_qty}
        else:
            res = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        return res

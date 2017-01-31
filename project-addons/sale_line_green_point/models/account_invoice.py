# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, _, exceptions


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def create_green_point_line(self):
        for inv in self:
            prod = self.env.ref('sale_line_green_point.product_green_point')
            # Delete green point lines to recalculate
            green_lines = inv.invoice_line.filtered(lambda l:
                                                    l.product_id.id == prod.id)
            green_lines.unlink()

            # Get the qty of green line products
            qty = 0.0
            for line in inv.invoice_line.filtered('product_id.green_point'):
                qty += line.quantity
            if qty:
                account_id = prod.property_account_income.id
                if not account_id:
                    account_id = prod.categ_id.property_account_income_categ.id
                    if not account_id:
                        raise exceptions.except_orm(
                            _('Error!'),
                            _('Please define income account for this \
                              product: "%s" (id:%d).') % (prod.name, prod.id,))
                    fpos = inv.fiscal_position or False
                    if fpos:
                        account_id = fpos.map_account(account_id)
                vals = {
                    'invoice_id': inv.id,
                    'product_id': prod.id,
                    'account_id': account_id,
                    'name': _('Green Point contribution'),
                    'quantity': qty,
                    'price_unit': prod.lst_price,
                    'uos_id': prod.uom_id.id,
                    'invoice_line_tax_id':
                    [(6, 0, [x.id for x in prod.taxes_id])]
                }
                self.env['account.invoice.line'].create(vals)
        return

    @api.multi
    def write(self, vals):
        # Recalculate green point qty if order lines modified
        res = super(AccountInvoice, self).write(vals)
        if 'invoice_line' in vals:
            self.create_green_point_line()
        return res

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        res.create_green_point_line()
        return res

# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def fix_sale_lines_price(self):
        # Correcciones en pedidos 11/05/17
        for order in self.search([('name', 'in', ['SO335','SO333','SO300','SO287','SO191','SO336','SO267','SO344', 'SO200'])]):
            for line in order.order_line:
                if line.invoice_lines:
                    if line.price_unit != line.invoice_lines[0].price_unit or order.name == 'SO200':
                        line.price_unit = line.invoice_lines[0].price_unit
                    if line.discount1 != line.invoice_lines[0].discount1 or order.name == 'SO200':
                        line.discount1 = line.invoice_lines[0].discount1
                    if line.discount2 != line.invoice_lines[0].discount2 or order.name == 'SO200':
                        line.discount2 = line.invoice_lines[0].discount2
                    if line.discount3 != line.invoice_lines[0].discount3 or order.name == 'SO200':
                        line.discount3 = line.invoice_lines[0].discount3
                    if line.discount4 != line.invoice_lines[0].discount4 or order.name == 'SO200':
                        line.discount4 = line.invoice_lines[0].discount4
        self.env['sale.order.line'].browse(193).price_unit = 25.0
        self.env['sale.order'].browse(271).order_line.write({'price_unit': 0})
        self.env['sale.order.line'].browse(531).write({'price_unit': 19.2000, 'discount1': 28.33})

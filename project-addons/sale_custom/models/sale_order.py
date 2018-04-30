# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api

from openerp.osv import fields as fields2, osv


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    expedition_date = fields.Date('Expedition Date', required=True)

    @api.multi
    def fix_sale_lines_price(self):
        # Correcciones en pedidos 11/05/17
        solist = ['SO335', 'SO333', 'SO300', 'SO287', 'SO191', 'SO336',
                  'SO267', 'SO344', 'SO200']
        for order in self.search([('name', 'in', solist)]):
            for line in order.order_line:
                if line.invoice_lines:
                    if line.price_unit != line.invoice_lines[0].price_unit or \
                            order.name == 'SO200':
                        line.price_unit = line.invoice_lines[0].price_unit
                    if line.discount1 != line.invoice_lines[0].discount1 or \
                            order.name == 'SO200':
                        line.discount1 = line.invoice_lines[0].discount1
                    if line.discount2 != line.invoice_lines[0].discount2 or \
                            order.name == 'SO200':
                        line.discount2 = line.invoice_lines[0].discount2
                    if line.discount3 != line.invoice_lines[0].discount3 or \
                            order.name == 'SO200':
                        line.discount3 = line.invoice_lines[0].discount3
                    if line.discount4 != line.invoice_lines[0].discount4 or \
                            order.name == 'SO200':
                        line.discount4 = line.invoice_lines[0].discount4
        self.env['sale.order.line'].browse(193).price_unit = 25.0
        self.env['sale.order'].browse(271).order_line.write({'price_unit': 0})
        self.env['sale.order.line'].browse(531).write({'price_unit': 19.2000,
                                                       'discount1': 28.33})


class SaleOrderDatesOldApi(osv.osv):
    """Overwrited old api"""
    _inherit = 'sale.order'

    def _get_effective_date(self, cr, uid, ids, name, arg, context=None):
        """OVERWRITED, only pickings processed"""
        res = {}
        dates_list = []
        for order in self.browse(cr, uid, ids, context=context):
            dates_list = []
            for pick in order.picking_ids:
                if pick.state == 'done':
                    dates_list.append(pick.date)
            if dates_list:
                res[order.id] = min(dates_list)
            else:
                res[order.id] = False
        return res

    _columns = {
        'effective_date': fields2.function(
            _get_effective_date, type='date',
            store=True, string='Effective Date',
            help="Date on which the first Delivery Order was created.")
    }

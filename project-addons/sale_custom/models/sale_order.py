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


class SaleReport(models.Model):

    _inherit = 'sale.report'

    expedition_date = fields.Date('Expedition Date', readonly=True)

    def _select(self):
        select_str = """
        WITH currency_rate (currency_id, rate, date_start, date_end) AS (
                SELECT r.currency_id, r.rate, r.name AS date_start,
                    (SELECT name FROM res_currency_rate r2
                    WHERE r2.name > r.name AND
                        r2.currency_id = r.currency_id
                     ORDER BY r2.name ASC
                     LIMIT 1) AS date_end
                FROM res_currency_rate r
            )
         SELECT min(l.id) as id,
                l.product_id as product_id,
                t.uom_id as product_uom,
                sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
                sum(l.product_uom_qty * l.price_unit / cr.rate * (100.0-l.discount) / 100.0) as price_total,
                count(*) as nbr,
                s.date_order as date,
                s.date_confirm as date_confirm,
                s.expedition_date as expedition_date,
                s.partner_id as partner_id,
                s.user_id as user_id,
                s.company_id as company_id,
                extract(epoch from avg(date_trunc('day',s.date_confirm)-date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2) as delay,
                l.state,
                t.categ_id as categ_id,
                s.pricelist_id as pricelist_id,
                s.project_id as analytic_account_id,
                s.section_id as section_id
        """
        return select_str

    def _group_by(self):
        group_by_str = """
            GROUP BY l.product_id,
                    l.order_id,
                    t.uom_id,
                    t.categ_id,
                    s.date_order,
                    s.date_confirm,
                    s.partner_id,
                    s.user_id,
                    s.company_id,
                    l.state,
                    s.pricelist_id,
                    s.project_id,
                    s.section_id,
                    s.expedition_date
        """
        return group_by_str
# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class SaleOrderAvailablePromos(models.Model):

    _name = 'sale.order.available.promos'

    sale_id = fields.Many2one('sale.order')
    applied = fields.Boolean(compute='_get_is_applied', store=True)
    promotion = fields.Many2one('promos.rules')

    @api.depends('sale_id.promo_discount1',
                 'sale_id.promo_discount2',
                 'sale_id.promo_discount3',
                 'sale_id.promo_discount4')
    def _get_is_applied(self):
        for av_promo in self:
            applied_promos = [av_promo.sale_id.promo_discount1.id,
                              av_promo.sale_id.promo_discount2.id,
                              av_promo.sale_id.promo_discount3.id,
                              av_promo.sale_id.promo_discount4.id]
            if av_promo.promotion.id in applied_promos:
                av_promo.applied = True
            else:
                av_promo.applied = False

    @api.multi
    def force_promotion(self):
        self.env['promos.rules'].execute_actions(
            self.promotion, self.sale_id.id)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
    available_promos = fields.One2many('sale.order.available.promos', 'sale_id')

    @api.multi
    def onchange_partner_id(self, part):
        res = super(SaleOrder, self).onchange_partner_id(part)
        if 'value' not in res:
            res['value'] = {}
        if not part:
            return res

        partner = self.env['res.partner'].browse(part)
        domain = self.env['promos.rules']._get_promotions_domain(
            self, partner, fields.Datetime.now())
        active_promos = self.env['promos.rules'].search(domain)
        available_promos = []
        for promo in active_promos:
            available_promos.append((0, 0, {'promotion': promo.id}))
        res['value']['available_promos'] = available_promos
        return res

    @api.multi
    def onchange_date_order(self, partner_id, date_order):
        if not partner_id:
            return
        partner = self.env['res.partner'].browse(partner_id)
        domain = self.env['promos.rules']._get_promotions_domain(
            self, partner, date_order)
        active_promos = self.env['promos.rules'].search(domain)
        available_promos = []
        for promo in active_promos:
            available_promos.append((0, 0, {'promotion': promo.id}))
        return {'value': {'available_promos': available_promos}}

    @api.multi
    def get_free_discount_field(self, promo):
        self.ensure_one()
        res = ''
        if promo.id == self.promo_discount1.id or not self.promo_discount1:
            res = 'discount1'
        elif promo.id == self.promo_discount2.id or not self.promo_discount2:
            res = 'discount2'
        elif promo.id == self.promo_discount3.id or not self.promo_discount3:
            res = 'discount3'
        elif promo.id == self.promo_discount4.id or not self.promo_discount4:
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
        for line in order.order_line:
            line.write({
                'discount1': 0,
                'discount2': 0,
                'discount3': 0,
                'discount4': 0,
            })
        return res

    @api.model
    def _prepare_invoice(self, order, lines):
        res = super(SaleOrder, self).\
            _prepare_invoice(order, lines)

        note = ''
        if order.promo_discount1:
            note += "\n" + _('Discount 1: ') + order.promo_discount1.name
        if order.promo_discount2:
            note += "\n" + _('Discount 2: ') + order.promo_discount2.name
        if order.promo_discount3:
            note += "\n" + _('Discount 3: ') + order.promo_discount3.name
        if order.promo_discount4:
            note += "\n" + _('Discount 4: ') + order.promo_discount4.name
        res.update({
            'promo_discount1': order.promo_discount1.id,
            'promo_discount2': order.promo_discount2.id,
            'promo_discount3': order.promo_discount3.id,
            'promo_discount4': order.promo_discount4.id,
            'comment': note
        })
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
    discount1 = fields.Float('Disc. 1', copy=False,
                             digits=dp.get_precision('Discount'))
    discount2 = fields.Float('Disc. 2', copy=False,
                             digits=dp.get_precision('Discount'))
    discount3 = fields.Float('Disc. 3', copy=False,
                             digits=dp.get_precision('Discount'))
    discount4 = fields.Float('Disc. 4', copy=False,
                             digits=dp.get_precision('Discount'))

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

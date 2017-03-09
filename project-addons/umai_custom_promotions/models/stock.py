# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, _


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        res = super(StockPicking, self).\
            _get_invoice_vals(key, inv_type, journal_id, move)
        if move.picking_id.sale_id:
            order = move.picking_id.sale_id

            note = ''
            if order.promo_discount1:
                note += _('Discount 1: ') + order.promo_discount1.name + "\n"
            if order.promo_discount2:
                note += _('Discount 2: ') + order.promo_discount2.name + "\n"
            if order.promo_discount3:
                note += _('Discount 3: ') + order.promo_discount3.name + "\n"
            if order.promo_discount4:
                note += _('Discount 4: ') + order.promo_discount4.name + "\n"
            res.update({
                'promo_discount1': order.promo_discount1.id,
                'promo_discount2': order.promo_discount2.id,
                'promo_discount3': order.promo_discount3.id,
                'promo_discount4': order.promo_discount4.id,
                'comment': note
            })
        return res


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.model
    def _get_invoice_line_vals(self, move, partner, inv_type):
        res = super(StockMove, self).\
            _get_invoice_line_vals(move, partner, inv_type)
        if move.procurement_id and move.procurement_id.sale_line_id:
            sl = move.procurement_id.sale_line_id
            res.update({
                'discount1': sl.discount1,
                'discount2': sl.discount2,
                'discount3': sl.discount3,
                'discount4': sl.discount4,
            })
        return res

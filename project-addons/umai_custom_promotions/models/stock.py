# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


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

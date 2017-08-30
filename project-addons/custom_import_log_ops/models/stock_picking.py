# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _
from openerp.addons import decimal_precision as dp


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sanmy_order = fields.Char("Nº Pedido Sanmy")
    sanmy_pick = fields.Char("Nº de albarán Sanmy")
    umai_order = fields.Many2one('sale.order')
    picking_type_code = fields.Selection(related="picking_type_id.code")

class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    partner_id = fields.Many2one('res.partner')
    code = fields.Selection(selection_add=[('logistic', 'Logistic Operation')])

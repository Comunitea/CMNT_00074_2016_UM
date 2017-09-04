# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class SaleConfigSettings(models.TransientModel):
    _inherit = 'sale.config.settings'

    @api.model
    def _get_default_gree_point(self):
        self.green_point_id = self.env['product.product']

    auto_sale_confirm = fields.Boolean('Confirmación ventas auto', default="True")
    auto_pick_confirm = fields.Boolean("Confirmación albaranes auto", default="True")
    green_point = fields.Boolean("Punto verde", default="True")
    green_point_id = fields.Many2one('product.product', 'Punto verde', default= 25)
    force_lot_id = fields.Boolean ("Forzar un lote", default="True")

# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields



class PartnerLogistic(models.Model):

    _name = "partner.logistic"
    _rec_name = "display_name"

    def _get_display_name(self):
        self.display_name = '%s (%s)'%(self.name, self.delivery_name)

    name = fields.Char("Name")
    delivery_name = fields.Char("Delivery Name")
    cp = fields.Char("Zip Code")
    state = fields.Char("State")
    city = fields.Char("City")
    display_name = fields.Char(compute=_get_display_name)
    partner_id = fields.Many2one('res.partner')



class SaleOrder(models.Model):

    _inherit = 'sale.order'

    logistic_partner_id = fields.Many2one('partner.logistic', "Cliente final")
    shipping_partner_id_type = fields.Char(related='partner_shipping_id.partner_type_id.name', readonly=1)
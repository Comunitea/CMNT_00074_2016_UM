# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, _


ACTION_TYPES = [
    ('prod_disc_perc', _('Discount % on Product')),
    ('prod_disc_fix', _('Fixed amount on Product')),
    ('cart_disc_perc', _('Discount % on Sub Total')),
    ('cart_disc_fix', _('Fixed amount on Sub Total')),
    ('prod_x_get_y', _('Buy X get Y free')),
    ('line_prod_disc_perc', _('New line discount, over order subtotal')),
    ('line_discount_group_price', _('New line discount, over price unit')),
    ('line_discount_mult_pallet', _('New line discount, multiply of pallet')),
    ('line_discount_columns', _('Discount per columns')),
]


class PromotionsRulesActions(models.Model):
    _inherit = 'promos.rules.actions'

    action_type = fields.Selection(ACTION_TYPES, 'Action', required=True)

    @api.multi
    def action_line_discount_columns(self, order):
        import ipdb; ipdb.set_trace()
        return
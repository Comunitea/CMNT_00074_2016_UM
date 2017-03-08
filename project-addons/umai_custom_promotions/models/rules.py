# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero Fernández <javier@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, _
from openerp.exceptions import except_orm

ACTION_TYPES = [
    ('prod_disc_perc', _('Discount % on Product')),
    ('prod_disc_fix', _('Fixed amount on Product')),
    ('cart_disc_perc', _('Discount % on Sub Total')),
    ('cart_disc_fix', _('Fixed amount on Sub Total')),
    ('prod_x_get_y', _('Buy X get Y free')),
    ('line_prod_disc_perc', _('New line discount, over order subtotal')),
    ('line_discount_group_price', _('New line discount, over price unit')),
    ('line_discount_mult_pallet', _('New line discount, multiply of pallet')),
    ('line_discount_columns', _('Discount distributed in columns')),
    ('line_discount_columns_mult_pallet', _('Discount distributed in columns,\
                                             multiply of pallet')),
]


class PromotionsRulesActions(models.Model):
    _inherit = 'promos.rules.actions'

    action_type = fields.Selection(ACTION_TYPES, 'Action', required=True)

    @api.model
    def action_line_discount_columns(self, action, order):
        """
        Crea hasta 4 descuentos, en la misma línea si esta cumple que es un
        pallet,
        cada uno en una columna para las promociones implicadas.
        """

        selected_lines = []
        restrict_codes = False
        if action.product_code:
            restrict_codes = action.product_code.replace("'", '').split(',')
        for line in order.order_line.\
                filtered(lambda l: not l.product_id.no_promo):
            if restrict_codes and line.product_id.code not in restrict_codes:
                continue
            selected_lines += line
        self._create_discounts_in_columns(action, order, selected_lines)

    @api.model
    def action_line_discount_columns_mult_pallet(self, action, order):

        """
        Crea hasta 4 descuentos, en la misma línea,
        cada uno en una columna para las promociones implicadas.
        """
        selected_lines = []
        for line in order.order_line.\
                filtered(lambda l: not l.product_id.no_promo):
            packing = line.product_id.packaging_ids \
                and line.product_id.packaging_ids[0] or False
            num_pallets = 0.0
            if packing and packing.ul.type == 'pallet' and packing.qty:
                num_pallets = line.product_uom_qty / packing.qty
            if not num_pallets or num_pallets % 1 != 0:
                continue

            selected_lines += line
        self._create_discounts_in_columns(action, order, selected_lines)
        return

    @api.model
    def _create_discounts_in_columns(self, action, order, selected_lines):
        """
        Crea hasta 4 descuentos, en la misma línea,
        cada uno en una columna para las promociones implicadas.
        """
        discount = eval(action.arguments)
        promo = action.promotion
        discount_field = order.get_free_discount_field(promo)
        if not discount_field:
            raise except_orm(_('Error'), _('All discount fields used, can not\
                set discount for promotion %s') % promo.name)
        for line in selected_lines:
            line.write({discount_field: discount})

        promo_discount_field = 'promo_' + discount_field
        order.write({promo_discount_field: promo.id})
        return

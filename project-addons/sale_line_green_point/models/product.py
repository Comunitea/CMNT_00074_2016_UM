# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ProductProduct(models.Model):

    _inherit = 'product.product'

    green_point = fields.Boolean('Green Point', help='If checked the product \
        will be used to compute the green point line in the sale order')

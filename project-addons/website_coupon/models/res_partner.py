# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    applied_coupon = fields.One2many(
        'partner.coupon', 'partner_id', string="Coupons Applied")

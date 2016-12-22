# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _
from ast import literal_eval

class ResUsers(models.Model):

    _inherit = 'res.users'

    @api.model
    def _signup_create_user(self, values):
        res = super(ResUsers, self)._signup_create_user(values)
        self.browse(res).partner_id.website_partner = True
        return res

    @api.multi
    def copy(self, default={}):
        res = super(ResUsers, self).copy(default)
        ir_config_parameter = self.env['ir.config_parameter']
        template_user_id = literal_eval(ir_config_parameter.get_param('auth_signup.template_user_id', 'False'))
        if self.id == template_user_id:
            res.property_product_pricelist = self.property_product_pricelist
            res.property_account_position = self.property_account_position
        return res

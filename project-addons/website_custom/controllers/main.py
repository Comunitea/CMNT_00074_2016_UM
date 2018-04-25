# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.website_sale.controllers.main import website_sale
from openerp.http import request

class website_sale_custom_fields(website_sale):

    def checkout_form_validate(self, data):
        if 'vat' in data:
            data['vat'] = data['vat'].replace('-', '').upper()
        res = super(website_sale_custom_fields, self).checkout_form_validate(data)
        if not data.get('phone') and not data.get('mobile'):
            res['phone'] = 'missing'
            res['mobile'] = 'missing'
        if not data.get('firstname'):
            res['firstname'] = 'missing'
        if not data.get('lastname'):
            res['lastname'] = 'missing'
        if data.get("shipping_id") == -1:
            if not data.get('shipping_phone') and not data.get('shipping_mobile'):
                res['shipping_phone'] = 'missing'
                res['shipping_mobile'] = 'missing'
        return res

    def _get_mandatory_billing_fields(self):
        res = super(website_sale_custom_fields, self)._get_mandatory_billing_fields()
        return [x for x in res if x not in  ('name', 'phone')] + ['firstname', 'lastname']

    def _get_optional_billing_fields(self):
        return super(
            website_sale_custom_fields,
            self)._get_optional_billing_fields()  + ["phone", "mobile"]

    def _get_mandatory_shipping_fields(self):
        res = super(
            website_sale_custom_fields, self)._get_mandatory_shipping_fields()
        return [x for x in res if x != 'phone']

    def _get_optional_shipping_fields(self):
        return super(
            website_sale_custom_fields,
            self)._get_optional_shipping_fields() + ["phone", "mobile"]

    def checkout_parse(self, address_type, data, remove_prefix=False):
        res = super(website_sale_custom_fields,self).checkout_parse(address_type, data, remove_prefix=remove_prefix)
        template_user_id = request.env['ir.config_parameter'].get_param('auth_signup.template_user_id')
        template_user = request.env['res.users'].browse(int(template_user_id)).sudo()
        if template_user:
            res['property_product_pricelist'] = template_user.property_product_pricelist.id
            res['property_account_position'] = template_user.property_account_position.id
            res['website_partner'] = True
            res['user_id'] = template_user.user_id.id
            res['category_id'] = [(6, 0, [x.id for x in template_user.category_id])]
            order = request.website.sale_get_order(force_create=1)
            order.write({'user_id': res['user_id']})
        return res

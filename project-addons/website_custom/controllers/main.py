# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.website_sale.controllers.main import website_sale


class website_sale_custom_fields(website_sale):

    def checkout_form_validate(self, data):
        res = super(website_sale_custom_fields, self).checkout_form_validate(data)
        if not data.get('phone') and not data.get('mobile'):
            res['phone'] = 'missing'
            res['mobile'] = 'missing'
        if data.get("shipping_id") == -1:
            if not data.get('shipping_phone') and not data.get('shipping_mobile'):
                res['shipping_phone'] = 'missing'
                res['shipping_mobile'] = 'missing'
        return res

    def _get_mandatory_billing_fields(self):
        res = super(website_sale_custom_fields, self)._get_mandatory_billing_fields()
        return [x for x in res if x != 'phone']

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

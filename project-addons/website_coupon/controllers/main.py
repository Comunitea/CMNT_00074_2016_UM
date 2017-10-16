# -*- coding: utf-8 -*-

from openerp import http
from openerp.http import request
from datetime import datetime
from dateutil import parser

import openerp.addons.website_sale.controllers.main


class WebsiteCoupon(openerp.addons.website_sale.controllers.main.website_sale):

    @http.route(['/shop/gift_coupon'], type='http', auth="public", website=True)
    def gift_coupon(self, promo_voucher, **post):
        """This function will be executed when we click the apply button of
        the voucher code in the website. It will verify the validity and
        availability of that coupon. If it can be applied, the coupon
        will be applied and coupon balance will also be updated"""
        curr_partner = request.env.user.partner_id
        coupon = request.env['gift.coupon'].sudo().search([('code', '=', promo_voucher)], limit=1)
        apply_discount = True
        if coupon and coupon.total_avail > 0:
            applied_coupons = request.env['partner.coupon'].sudo().search(
                [('coupon', '=', promo_voucher),
                 ('partner_id', '=', curr_partner.id)], limit=1)

        # checking voucher date and limit for each user for this coupon
            if coupon.partner_id:
                if curr_partner.id != coupon.partner_id.id:
                    apply_discount = False
            today = datetime.now().date()
            if apply_discount and applied_coupons.number < coupon.limit and \
                    today <= parser.parse(coupon.voucher.expiry_date).date():
                # checking coupon validity
                #    checking date of coupon
                if coupon.start_date and coupon.end_date:
                    if today < parser.parse(coupon.start_date).date() or \
                            today > parser.parse(coupon.end_date).date():
                        apply_discount = False
                elif coupon.start_date:
                    if today < parser.parse(coupon.start_date).date():
                        apply_discount = False
                elif coupon.end_date:
                    if today > parser.parse(coupon.end_date).date():
                        apply_discount = False
            else:
                apply_discount = False
        else:
            apply_discount = False
        if apply_discount:
            voucher_type = coupon.voucher.voucher_type
            voucher_val = coupon.voucher_val
            type = coupon.type
            coupon_product = request.env.ref('website_coupon.discount_product')
            if coupon_product:
                order = request.website.sale_get_order(force_create=1)
                applicable_discount = False
                for line in order.order_line:
                    if line.product_id.id == coupon_product.id:
                        apply_discount = False
                        break
                if apply_discount and order.order_line:
                    if voucher_type == 'product':
                        # the voucher type is product
                        product_id = coupon.voucher.product_id
                        for line in order.order_line:
                            if line.product_id.id == product_id.id:
                                    applicable_discount = True
                    elif voucher_type == 'category':
                        # the voucher type is category
                        categ_id = coupon.voucher.product_categ
                        for line in order.order_line:
                            if line.product_id.categ_id.id == categ_id.id:
                                applicable_discount = True
                    elif voucher_type == 'all':
                        # the voucher is applicable to all products
                        applicable_discount = True
                    if applicable_discount:
                        # the voucher is applicable
                        if type == 'fixed':
                            # coupon type is 'fixed'
                            if voucher_val < order.amount_total:
                                discount_amount = -voucher_val
                            else:
                                return request.redirect("/shop/coupon?coupon_not_available=3")
                        elif type == 'percentage':
                            # coupon type is percentage
                            amount_final = (voucher_val/100) * order.amount_total
                            discount_amount = -amount_final
                        value = order._cart_update(product_id=coupon_product.id, set_qty=1)
                        disc_line = request.env['sale.order.line'].sudo().browse(value['line_id'])
                        disc_line.write({'price_unit': discount_amount, 'coupon_discount_line': True, 'name': '%s: %s' % (coupon_product.display_name,coupon.name)})

                        # updating coupon balance
                        total = coupon.total_avail - 1
                        coupon.write({'total_avail': total})

                        if not applied_coupons:
                            curr_partner.write(
                                {'applied_coupon':
                                 [(0, 0, {'partner_id': curr_partner.id,
                                          'coupon': coupon.code,
                                          'number': 1})]})
                        else:
                            applied_coupons.write(
                                {'number': applied_coupons.number + 1})
                    else:
                        return request.redirect(
                            "/shop/coupon?coupon_not_available=1")
                else:
                    return request.redirect(
                        "/shop/coupon?coupon_not_available=2")
        else:
            return request.redirect("/shop/coupon?coupon_not_available=1")

        return request.redirect("/shop/coupon")

    @http.route(['/shop/coupon'], type='http', auth="user", website=True)
    def coupon(self, **post):
        values = {}
        if post.get('coupon_not_available'):
            values['coupon_not_available'] = post.get('coupon_not_available')
        return request.website.render("website_coupon.cart_coupons", values)

# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import models


def copy_discount_column(cr, registry):
    """This post-init-hook copy update all discount columns to
    the new discount 1"""
    cr.execute("""
        UPDATE account_invoice_line
        SET discount1 = discount
        """)
    cr.execute("""
        UPDATE sale_order_line
        SET discount1 = discount
        """)

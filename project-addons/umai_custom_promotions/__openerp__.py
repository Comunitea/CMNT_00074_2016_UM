# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'UMAI Custom Promotions',
    'version': '8.0.0.0.0',
    'author': 'Comunitea ',
    "category": "Custom",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale_promotions',
        'stock_account'
    ],
    'contributors': [
        "Comunitea ",
        "Javier Colmenero <javier@comunitea.com>"
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/invoice_view.xml",
        "security/ir.model.access.csv"
    ],
    "demo": [
    ],
    'test': [
    ],
    "installable": True,
    "post_init_hook": "copy_discount_column",
}

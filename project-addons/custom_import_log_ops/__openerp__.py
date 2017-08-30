# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "ODOO xls import logistic operations",
    "summary": "Importacion de picking de operador logistico",
    "version": "8.0.1.0.0",
    "category": "Stock",
    "website": "comunitea.com",
    "author": "Comunitea",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
        'stock'
    ],
    "data": [
        'wizard/wzd_log_ops.xml',
        'views/logistic_operation.xml',
        'data/stock_picking_type.xml',
        'views/sale_view.xml',
        'security/ir.model.access.csv'
    ],
}

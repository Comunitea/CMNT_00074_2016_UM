# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields

try:
    from openerp.addons.report_xlsx.report.report_xlsx import ReportXlsx
except ImportError:
    class ReportXlsx(object):
        def __init__(self, *args, **kwargs):
            pass

class LogisticPickingXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, pickings):
        sheet = workbook.add_worksheet('1')
        bold = workbook.add_format({'bold': True})
        pos = 1
        header = [u'SALES ORDER', u'ORDER SENDING DATE', u'TIME',
                  u'ORDER RECEIVING DATE ', u'PICKING DATE',
                  u'EXPEDITION DATE', u'EXPECTED DELIVERY DATE ',
                  u'BOOKING DELIVERY TIME', u'REAL DELIVERY DATE',
                  u'REAL DELIVERY TIME', u'CUSTOMER NAME', u'CUSTOMER CODE',
                  u'DELIVERY ADDRESS', u'P.C.', u'CITY', u'COUNTRY',
                  u'CONTACT PERSON', u'PHONE Nº', u'CUSTOMER ITEM Nº',
                  u'UMAI CHA ITEM Nº', u'DESCRIPTION', u'QUANTITY (PACK 12)',
                  u'WEIGHT', u'LOT', u'EXPIRATION DATE ', u'COURIER',
                  u'COMMENT 1', u'COMMENT 2', u'COMMENT 3']
        sheet.write_row(0, 0, header)
        for pick in pickings:
            min_date = fields.Datetime.from_string(pick.min_date).strftime('%m/%d/%Y')
            order_date = order_hour = False
            if pick.sale_id:
                order_date = fields.Datetime.from_string(pick.sale_id.date_order).strftime('%m/%d/%Y')
                order_hour = fields.Datetime.from_string(pick.sale_id.date_order).strftime('%H:%M:%S')
            phone = pick.partner_id.phone or pick.partner_id.mobile
            if not phone:
                phone = pick.partner_id.commercial_partner_id.phone or \
                    pick.partner_id.commercial_partner_id.mobile
            if pick.pack_operation_ids:
                for op in pick.pack_operation_ids:
                    life_date = ''
                    if op.lot_id.use_date:
                        life_date = fields.Datetime.from_string(op.lot_id.use_date).strftime('%m/%d/%Y')
                    picking_row = [pick.sale_id.name,
                                   order_date, order_hour, order_date, '', '',
                                   min_date, '', '', '', pick.partner_id.commercial_partner_id.name,
                                   pick.partner_id.ref,
                                   (pick.partner_id.street or '') + ' ' +
                                   (pick.partner_id.street2 or ''),
                                   pick.partner_id.zip, pick.partner_id.city,
                                   pick.partner_id.country_id.name,
                                   pick.partner_id.name,
                                   phone,
                                   '', op.product_id.default_code,
                                   op.product_id.name, op.product_qty,
                                   op.product_qty * op.product_id.weight_net,
                                   op.lot_id.name, life_date,
                                   pick.carrier_id.name or '']
                    sheet.write_row(pos, 0, picking_row)
                    pos += 1
            else:
                for move in pick.move_lines:
                    life_date = ''
                    lot = move.procurement_id.lot_id
                    if lot.use_date:
                        life_date = fields.Datetime.from_string(lot.use_date).strftime('%m/%d/%Y')
                    picking_row = [pick.sale_id.name,
                                   order_date, order_hour, order_date, '', '',
                                   min_date, '', '', '', pick.partner_id.commercial_partner_id.name,
                                   pick.partner_id.ref,
                                   (pick.partner_id.street or '') + ' ' +
                                   (pick.partner_id.street2 or ''),
                                   pick.partner_id.zip, pick.partner_id.city,
                                   pick.partner_id.country_id.name,
                                   pick.partner_id.name,
                                   phone,
                                   '', move.product_id.default_code,
                                   move.product_id.name, move.product_uom_qty,
                                   move.product_uom_qty * move.product_id.weight_net,
                                   lot.name, life_date,
                                   pick.carrier_id.name or '']
                    sheet.write_row(pos, 0, picking_row)
                    pos += 1

        for i in range(len(header)):
            sheet.set_column(i, 0,20)


LogisticPickingXlsx('report.stock.picking.xlsx', 'stock.picking')

# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _

AUTO_SALE_CONFIRM = True
AUTO_PICK_CONFIRM = True
GREEN_POINT = True
GREEN_POINT_ID = 25
FORCE_LOT_ID = True


class LogisticOperation(models.Model):

    _name = 'logistic.operation'

    ack = fields.Boolean("Ack", default=False)
    partner_id = fields.Many2one('res.partner')
    nombre_cliente = fields.Char('Nombre Cliente')
    product_id = fields.Many2one('product.product')
    nombre_envio = fields.Char("Dirección envío")
    cp_envio = fields.Char("Cp envío")
    provincia_envio = fields.Char("Provincia envío")
    poblacion_envio = fields.Char("Poblacion envío")
    cod_articulo = fields.Char('Codigo Sanmy')
    ref_articulo_cliente = fields.Char("Codigo UMAI")
    articulo = fields.Char("Descripción artículo")
    num_ped_sanmy = fields.Char("Numero pedido Sanmy")
    num_pedido = fields.Char("Numero pedido UMAI")
    albaran = fields.Char("Fecha albarçan Sanmy ")
    fecha_albaran = fields.Date("Fecha albaránn Sanmy ")
    factura = fields.Char("Factura (0)")
    lote = fields.Char("Lote")
    caducidad = fields.Date("Fecha de caducidad")
    cantidad = fields.Float("Cantidad (uds)")




    @api.multi
    def import_selected(self):
        #HARDCODEADO POR QUE HAY 2 GREEN POINT

        sale_order_sanmy = [x.num_ped_sanmy for x in self]
        sale_order_ids = list(set(sale_order_sanmy))
        ret_sale_order_ids =[]
        for num_ped_sanmy in sale_order_ids:
            domain = [('client_order_ref', '=', num_ped_sanmy), ('state', '!=', 'cancel')]
            sale_order = self.env['sale.order'].search(domain)
            for op in self.filtered(lambda x: x.ack == False and x.num_ped_sanmy == num_ped_sanmy):
                if not sale_order:
                    vals = self.get_sale_order_values(op)
                    sale_order = self.env['sale.order'].create(vals)
                    ret_sale_order_ids.append(sale_order.id)
                if sale_order:
                    vals = self.get_sale_order_line_values(op, sale_order.id)
                    sale_order_line = self.env['sale.order.line'].create(vals)
                    if sale_order_line:
                        op.ack = True

        if AUTO_SALE_CONFIRM:
            for order_to_confirm in self.env['sale.order'].browse(ret_sale_order_ids):
                if GREEN_POINT:
                    qtys = sum(line.product_uom_qty for line in order_to_confirm.order_line)
                    vals = {
                        'product_id': GREEN_POINT_ID,
                        'product_uom_qty': qtys,
                        'order_id': order_to_confirm.id
                    }
                    self.env['sale.order.line'].create(vals)
                order_to_confirm.action_button_confirm()
        if AUTO_PICK_CONFIRM:
            for order_to_confirm in self.env['sale.order'].browse(ret_sale_order_ids):
                for pick in order_to_confirm.picking_ids:
                    pick.action_assign()
                    pick.force_assign()
                    pick.do_prepare_partial()
                    if FORCE_LOT_ID:
                        transfer = True
                        for pack_operation in pick.pack_operation_ids:
                            print pack_operation.product_id, pack_operation.lot_id.name
                            order_lines = order_to_confirm.order_line.filtered(lambda x:x.product_id == pack_operation.product_id)
                            for order_line in order_lines:
                                if order_line.product_id.id != GREEN_POINT_ID:
                                    if order_line.lot_id:
                                        pack_operation.lot_id = order_line.lot_id
                                    else:
                                        pack_operation.lot_id = False
                                        transfer = False
                        if transfer:
                            pick.do_transfer()
        view_id = self.env.ref('sale.view_quotation_tree')
        return {'type': 'ir.actions.act_window',
                'name': _('Sale Order'),
                'view_mode': 'tree,form',
                'view_type': 'form',
                'view_id': False,
                'res_model': 'sale.order',
                'domain': [('id', 'in', ret_sale_order_ids)]
                }

    @api.model
    def get_sale_order_line_values(self, op, order_id):
        domain = [('name', '=', op.lote), ('product_id', '=', op.product_id.id),
                  ('life_date', '>=', op.caducidad +" 00:00:01"), ('life_date','<=', op.caducidad +" 23:59:59")]
        lot_id = self.env['stock.production.lot'].search(domain, limit=1)
        # print "Busco lote para %s"%lot_id
        # for lot in lot_id:
        #     print lot.name, lot.life_date
        # if len(lot_id) != 1:
        #     lot_id = False
        product_id = op.product_id
        product_uom_qty = op.cantidad
        vals = {
            'product_id': product_id.id,
            'lot_id': lot_id and lot_id.id or False,
            'product_uom_qty': product_uom_qty,
            'order_id': order_id
        }
        return vals




    @api.model
    def get_sale_order_values(self, op):

        partner_shipping_id = op.partner_id.child_ids.filtered(lambda x: x.partner_type_id.name == 'Delivery')
        logistic_partner_id = self.env['partner.logistic'].search([('name', '=', op.nombre_cliente),
                                                                 ('delivery_name', '=', op.nombre_envio),
                                                                 ('partner_id', '=', op.partner_id.id)])

        if not logistic_partner_id:
            vals = {
                   'name': op.nombre_cliente,
                   'delivery_name': op.nombre_envio,
                   'cp': op.cp_envio,
                   'state': op.provincia_envio,
                   'city': op.poblacion_envio,
                   'partner_id': op.partner_id.id
            }

            logistic_partner_id = self.env['partner.logistic'].create(vals)

        client_order_ref = op.num_ped_sanmy
        origin = "SANMY: %s (%s)" %(op.num_pedido, op.albaran)
        vals = {
            'partner_id': op.partner_id.id,
            'partner_invoice_id': op.partner_id.id,
            'partner_shipping_id': partner_shipping_id.id,
            'logistic_partner_id': logistic_partner_id.id,
            'client_order_ref': client_order_ref,
            'origin': origin,
            'date_order': fields.Date.from_string(op.fecha_albaran.replace('/','-'))
        }
        return vals



    @api.multi
    def albaranar(self):
        picking_type = self.env.ref('custom_import_log_ops.picking_type_log_operation')
        location_id = picking_type.default_location_src_id
        location_dest_id = picking_type.default_location_dest_id
        partner_id = picking_type.partner_id or False

        for op in self:
            #usco el albarán de sanmy
            domain = [('sanmy_order', '=', op.num_ped_sanmy)]
            pick = self.env['stock.picking'].search(domain)
            domain = [('name','=', 'op.num_pedido')]
            sale_order = self.env['sale.order'].search(domain)
            if not pick:
                new_pick_vals = {
                    'picking_type_id': picking_type.id,
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    'partner_id': partner_id.id,
                    'sanmy_order': op.num_ped_sanmy,
                    'sanmy_pick': op.sanmy_pick,
                    'umai_order': umai_order and umai_order.id,
                    'date_done': op.strftime('%Y-%m-%d'),
                    'origin': umai_order and umai_order.name or op_num_ped_sanmy
                }
                new_pick = pick.create(new_pick_vals)

            default_code = self.ref_articulo_cliente[4:]
            product_domain = [('default_code', '=', default_code)]
            product_id = self.env['product.product'].search(product_domain)
            if not product_id:
                continue
                lot_id = self.env['stock.production.lot'].search([('name', '=', op.lote)])
                val_op = {
                    'product_id': product_id.id,
                    'location_id': location_id.id,
                    'location_dest_id': location_dest_id.id,
                    'picking_id': pick.id,
                    'product_qty': op.cantidad/12,
                    'qty_done': op.cantidad/12,
                    'product_uom_id': product_id.uom_id.id,
                    'lot_id': lot_id and lot_id.id or False,
                    'date': pick.date_done
                }
                self.env['stock.pack.operation'].create(val_op)
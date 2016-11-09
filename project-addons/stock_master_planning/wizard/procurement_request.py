# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################


import openerp.addons.decimal_precision as dp
from openerp import models, fields, api


class WizStockProcurementRequest(models.TransientModel):
    _name = "stock.procurement.request"
    _description = "Procurement request"

    product_id = fields.Many2one('product.product',
            string='Product',
            required=True, select=True)
    product_qty = fields.Float('Quantity', 
            digits_compute=dp.get_precision('Product Unit of Measure'),
            required=True)
    period_id = fields.Many2one('stock.planning.period', 
            string='Period', required=True)
    planning_detail_id = fields.Many2one('stock.planning.detail', 
            string='Period', required=True)
    procurement_date = fields.Date("Procurement date")

    @api.model
    def default_get(self, fields):
        res = super(WizStockProcurementRequest, self).default_get(fields)
        detail_plan_obj = self.env['stock.planning.detail']
        detail = detail_plan_obj.browse(self.env.context.get('active_id'))
        
        if 'product_id' in fields:
            res.update({'product_id': detail.product_id.id})
        if 'product_qty' in fields:
            res.update({'product_qty': detail.needed_qty})
        if 'period_id' in fields:
           res.update({'period_id': detail.period_id.id})
        if 'planning_detail_id' in fields:
           res.update({'planning_detail_id': detail.id})
        if 'procurement_date' in fields:
           res.update({'procurement_date': detail.period_id.start_date})
        return res

    @api.multi
    def generate_procurement(self):
        vals = self._prepare_procurement_vals()
        vals_group = self._prepare_procurement_group_vals()
        procurement_group_obj = self.env['procurement.group']
        procurement_obj = self.env['procurement.order']
        proc_group = procurement_group_obj.create(vals_group)
        vals['group_id'] = proc_group.id
        proc = procurement_obj.create(vals)
        proc.run()
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def _prepare_procurement_vals(self):
        return {
            'name': 'MPS/'+ self.period_id.name,
            'origin': 'MPS/'+ self.period_id.name,
            'date_planned': self.period_id.start_date,
            'product_id': self.product_id.id,
            'product_qty': self.product_qty,
            'product_uom': self.product_id.uom_id.id,
            'product_uos_qty': self.product_qty,
            'product_uos': self.product_id.uom_id.id,
            'company_id': self.planning_detail_id.planning_id.warehouse_id.company_id.id,
            'warehouse_id': self.planning_detail_id.planning_id.warehouse_id.id,
            'location_id': self.planning_detail_id.location_id.id,
            #'partner_dest_id': self.planning_detail_id.location_id.partner_id.id
        }

    @api.multi
    def _prepare_procurement_group_vals(self):
        return {
            'name': 'MPS/' + self.period_id.name
        }

        

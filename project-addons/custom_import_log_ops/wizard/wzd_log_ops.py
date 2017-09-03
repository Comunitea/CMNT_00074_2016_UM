# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _
from openerp.addons import decimal_precision as dp
import tempfile
import base64
import csv




class WzdLogOps(models.TransientModel):

    _name = 'wzd.log.ops'


    def _get_partner_domain(self):

        domain = [('partner_type_id', '=', 'Delivery')]
        partner_ids = self.env['res.partner'].search(domain)
        res = [('id', 'in', [x.parent_id.id for x in partner_ids])]
        return res


    def _get_partner_default(self):
        domain = [('partner_type_id', '=', 'Delivery')]
        partner_id = self.env['res.partner'].search(domain, limit=1)
        return partner_id.parent_id

    data = fields.Binary('File')
    delimiter = fields.Selection(
            [(',', ','), (';', ';'), ('|', '|')],
            string="CSV delimiter", default=",",
            required=True)
    partner_id = fields.Many2one('res.partner', domain=_get_partner_domain, default=_get_partner_default)


    @api.multi
    def import_file(self):

        def dec_row(value):

            res = value.decode("UTF-8").encode("latin_1").strip()
            return res

        with tempfile.TemporaryFile('w+b') as src:

            imp = self.read(['data', 'delimiter'])[0]
            content = imp['data']
            delimiter = imp['delimiter']
            src.write(content)
            with tempfile.TemporaryFile() as decoded:
                src.seek(0)
                base64.decode(src, decoded)
                decoded.seek(0)
                head, values = self._prepare_csv_data(decoded, delimiter)

        header = False
        ops = []
        row_number = 0
        for row in values:

            row_number +=1
            product_id = False
            product_code = dec_row(row[6])[4:].strip()
            if product_code:
                domain = [('default_code', '=', product_code)]
                product_id = self.env['product.product'].search(domain, limit = 1)
            if not product_id:
                continue

            #envío
            nombre_cliente = dec_row(row[0])
            nombre_envio = dec_row(row[1])
            cp_envio = dec_row(row[2])
            poblacion_envio = dec_row(row[3])
            provincia_envio = dec_row(row[4])
            #arituclo
            ref_cliente = dec_row(row[5])
            articulo = dec_row(row[7])
            #pedido/alabran
            num_ped_sanmy = dec_row(row[8])
            num_pedido = dec_row(row[9])
            albaran = dec_row(row[10])
            fecha_albaran = dec_row(row[11])
            mes = dec_row(row[12])
            factura = dec_row(row[13])
            lote =  dec_row(row[14])
            caducidad = dec_row(row[15])
            cantidad = float(dec_row(row[17]).replace(',', '.'))

            sale_order = num_pedido.strip()
            if sale_order:
                domain = [('name', '=', sale_order)]
                sale_order = self.env['sale.order'].search(domain)

                if sale_order:
                    continue
            if product_id:
                vals = {
                    'partner_id': self.partner_id.id,
                    'nombre_cliente': nombre_cliente,
                    'nombre_envio': nombre_envio,
                    'cp_envio': cp_envio,
                    'provincia_envio': provincia_envio,
                    'poblacion_envio': poblacion_envio,
                    'product_id': product_id.id,
                    'ref_articulo_cliente':  ref_cliente,
                    'cod_articulo': articulo,
                    'num_ped_sanmy': num_ped_sanmy,
                    'num_pedido':  num_pedido,
                    'albaran': albaran,
                    'fecha_albaran': fecha_albaran,
                    'factura': factura,
                    'lote': lote,
                    'caducidad':  caducidad,
                    'cantidad':  cantidad}

                new_op = self.env['logistic.operation'].create(vals)
                ops.append(new_op.id)

        return {'type': 'ir.actions.act_window',
                'name': _('Operations Order'),
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'logistic.operation',
                'domain': [('id', 'in', ops)]
                }

    @api.model
    def _prepare_csv_data(self, csv_file, delimiter=","):
        """Parse a decoded CSV file and return head list and data list

        :param csv_file: decoded CSV file
        :param delimiter: CSV file delimiter char
        :returns: (head [list of first row], data [list of list])

        """

        try:
            data = csv.reader((x.replace('\0', '') for x in csv_file),
                              delimiter=str(delimiter),
                              dialect=csv.excel_tab)
        except csv.Error as error:
            raise exceptions(
                _('CSV file is malformed'),
                _("Maybe you have not choose correct separator \n"
                  "the error detail is : \n %s") % repr(error)
            )

        head = data.next()
        head = [x.replace(' ', '') for x in head]
        # Generator does not work with orm.BaseModel.load
        values = [tuple(x) for x in data if x]
        return (head, values)



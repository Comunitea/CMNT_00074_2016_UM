# -*- coding: utf-8 -*-
# © 2016 Comunitea - Kiko Sanchez <kiko@comunitea.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _
from openerp.tools import html_escape as escape
from openerp.addons.base.ir.ir_qweb import HTMLSafe

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def formated_vat(self):
        """
        Si es código ES, se quita el ES se pone letra-numero
        Pero si no es ES, se poner FR-númeroLetra
        """
        formated_vat = ''
        if self.vat:
            if "ES" in self.vat:
                formated_vat = ("%s-%s") % (self.vat[-1], self.vat[2:10])
            else:
                formated_vat = ("%s-%s") % (self.vat[0:2], self.vat[2:11])
        return formated_vat


class Contact(models.AbstractModel):
    _inherit = 'ir.qweb.field.contact'

    def to_html(self, cr, uid, field_name, record, options,
                source_element, t_att, g_att, qweb_context, context=None):

        #necesitamos indicar cuando viene de account_invoice, ya que solo se vera el nif en account_invoice
        object = qweb_context['o']
        if object._name=="account.invoice":
            options['vat_in_header'] = True

        return super(Contact, self).to_html(cr = cr, uid=uid, field_name=field_name, record=record,
                                     options=options, source_element=source_element, t_att=t_att, g_att=g_att,
                                     qweb_context=qweb_context, context=context)



    def record_to_html(self, cr, uid, field_name, record, options=None, context=None):
        # necesitamos el valor de vat y formated_vat que no lo pasa a al val, por eso se hereda esta funcion
        if context is None:
            context = {}

        if options is None:
            options = {}
        opf = options.get('fields') or ["name", "address", "phone", "mobile", "fax", "email"]

        value_rec = record[field_name]
        if not value_rec:
            return None
        value_rec = value_rec.sudo().with_context(show_address=True)
        value = value_rec.name_get()[0][1]
        val = {
            'name': value.split("\n")[0],
            'address': escape("\n".join(value.split("\n")[1:])),
            'phone': value_rec.phone,
            'mobile': value_rec.mobile,
            'fax': value_rec.fax,
            'city': value_rec.city,
            'country_id': value_rec.country_id.display_name,
            'website': value_rec.website,
            'email': value_rec.email,
            'vat': value_rec.vat,
            'formated_vat': value_rec.formated_vat(),
            'fields': opf,
            'object': value_rec,
            'options': options
        }
        html = self.pool["ir.ui.view"].render(cr, uid, "base.contact", val, engine='ir.qweb', context=context).decode('utf8')

        return HTMLSafe(html)

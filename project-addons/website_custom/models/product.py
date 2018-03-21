# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    description_website = fields.Html(translate=True)
    feature_website = fields.Html(translate=True)
    image_list = fields.Binary()

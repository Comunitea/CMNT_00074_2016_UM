# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class ResPartner(models.Model):

    _inherit = 'res.partner'

    website_partner = fields.Boolean('Website partner')

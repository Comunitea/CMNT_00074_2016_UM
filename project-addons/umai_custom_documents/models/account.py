# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class ui(models.Model):

    _inherit = 'account.fiscal.position'

    vat = fields.Char()

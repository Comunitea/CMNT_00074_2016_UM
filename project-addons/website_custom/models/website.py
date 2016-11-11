# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class Website(models.Model):

    _inherit = 'website'

    social_instagram = fields.Char('Instagram account')


class WebsiteConfig(models.Model):

    _inherit = 'website.config.settings'


    social_instagram = fields.Char('Instagram account',
                                   related='website_id.social_instagram')

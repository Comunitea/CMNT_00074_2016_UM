# -*- coding: utf-8 -*-
# © 2016 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'UM website customizations',
    'summary': '',
    'version': '8.0.1.0.0',
    'category': 'Theme',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'website',
        'website_cmnt_custom_snippet',
        'theme_louma'
    ],
    'data': [
        'views/eshop_page.xml',
        'views/assets.xml',
        'views/customize_modal.xml',
        'views/footer.xml',
        'views/menu.xml',
        'views/page_contact.xml',
        'views/product.xml',
        'views/website.xml'
    ],
}

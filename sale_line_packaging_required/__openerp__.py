# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author

{
    "name": "Required Packaging on Sale Order Line",
    "version": "8.0.1.0.0",
    "author": "OpenSynergy Indonesia",
    "website": "https://opensynergy-indonesia.com",
    "license": "AGPL-3",
    "depends": [
        "sale_stock",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
}

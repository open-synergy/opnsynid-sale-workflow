# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Print Policy",
    "version": "8.0.1.0.0",
    "category": "Sale Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale",
        "base_print_policy"
    ],
    "data": [
        "data/res_groups.xml",
        "views/sale_order_views.xml"
    ],
}

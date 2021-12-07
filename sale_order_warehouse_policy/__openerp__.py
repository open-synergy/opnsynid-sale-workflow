# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Warehouse Policy",
    "version": "8.0.1.0.0",
    "category": "Purchase",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale_order_type",
    ],
    "data": [
        "views/sale_order_type_views.xml",
        "views/sale_order_views.xml",
    ],
}

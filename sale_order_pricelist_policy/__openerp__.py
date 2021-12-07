# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Sale Order Pricelist Policy",
    "version": "8.0.1.0.0",
    "category": "Sale Management",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["sale_order_type"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
    ],
}

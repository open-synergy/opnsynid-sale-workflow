# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Auto Create Project",
    "version": "8.0.1.0.0",
    "category": "Sale Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale_order_auto_create_contract",
        "project_task_template",
    ],
    "data": [
        "views/sale_order_type_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}

# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Product Policy",
    "version": "8.0.1.3.0",
    "category": "Sale",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base_action_rule",
        "sale_order_type",
    ],
    "data": [
        "data/ir_actions_server_data.xml",
        "data/base_action_rule_data.xml",
        "views/sale_order_type_views.xml",
        "views/sale_order_views.xml",
    ],
}

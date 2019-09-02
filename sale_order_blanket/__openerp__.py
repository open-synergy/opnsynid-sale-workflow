# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Blanket",
    "version": "8.0.1.2.0",
    "category": "Sale Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale_order_type",
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_document_version",
        "base_cancel_reason",
        "base_print_policy"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_workflow_policy_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        'wizards/create_sale_orders.xml',
        "views/sale_order_type_views.xml",
        "views/sale_order_blanket_views.xml",
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml",
    ],
}

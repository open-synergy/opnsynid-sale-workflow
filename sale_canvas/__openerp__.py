# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Sale Canvas",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_print_policy",
        "base_multiple_approval",
        "sale",
        "stock",
        "web_readonly_bypass",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "menu.xml",
        "views/canvas_type_views.xml",
        "views/canvas_route_views.xml",
        "views/canvas_order_views.xml",
        "views/canvas_order_detail_views.xml",
    ],
    "demo": [],
}

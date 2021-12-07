# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    invoice_recreate_group_ids = fields.Many2many(
        string="Allowed to Recreate Invoice",
        comodel_name="res.groups",
        rel="rel_sale_order_invoice_recreate",
        col1="type_id",
        col2="group_id",
    )
    invoice_corrected_group_ids = fields.Many2many(
        string="Allowed to Ignore Exception",
        comodel_name="res.groups",
        rel="rel_sale_order_invoice_corrected",
        col1="type_id",
        col2="group_id",
    )
    quotation_send_group_ids = fields.Many2many(
        string="Allowed to Send by Email",
        comodel_name="res.groups",
        rel="rel_sale_order_quotation_send",
        col1="type_id",
        col2="group_id",
    )
    confirm_order_group_ids = fields.Many2many(
        string="Allowed to Confirm Sale",
        comodel_name="res.groups",
        rel="rel_sale_order_confirm_order",
        col1="type_id",
        col2="group_id",
    )
    view_invoice_group_ids = fields.Many2many(
        string="Allowed to View Invoice",
        comodel_name="res.groups",
        rel="rel_sale_order_view_invoice",
        col1="type_id",
        col2="group_id",
    )
    create_invoice_group_ids = fields.Many2many(
        string="Allowed to Create",
        comodel_name="res.groups",
        rel="rel_sale_order_create_invoice",
        col1="type_id",
        col2="group_id",
    )
    copy_quotation_group_ids = fields.Many2many(
        string="Allowed to New Copy of Quotation",
        comodel_name="res.groups",
        rel="rel_sale_order_copy_quotation",
        col1="type_id",
        col2="group_id",
    )
    cancel_quot_group_ids = fields.Many2many(
        string="Allowed to Cancel Quotation",
        comodel_name="res.groups",
        rel="rel_sale_order_cancel_quot",
        col1="type_id",
        col2="group_id",
    )
    cancel_order_group_ids = fields.Many2many(
        string="Allowed to Cancel Order",
        comodel_name="res.groups",
        rel="rel_sale_order_cancel_order",
        col1="type_id",
        col2="group_id",
    )

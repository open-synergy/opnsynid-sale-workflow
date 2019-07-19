# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    blanket_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Blanket Sequence",
        copy=False,
    )
    blanket_confirm_group_ids = fields.Many2many(
        string="Allowed to Confirm",
        comodel_name="res.groups",
        rel="rel_sale_order_blanket_group_confirm",
        col1="type_id",
        col2="group_id",
    )
    blanket_approve_group_ids = fields.Many2many(
        string="Allowed to Approve",
        comodel_name="res.groups",
        rel="rel_sale_order_blanket_group_approve",
        col1="type_id",
        col2="group_id",
    )
    blanket_open_group_ids = fields.Many2many(
        string="Allowed to Open",
        comodel_name="res.groups",
        rel="rel_sale_order_blanket_group_open",
        col1="type_id",
        col2="group_id",
    )
    blanket_done_group_ids = fields.Many2many(
        string="Allowed to Finish",
        comodel_name="res.groups",
        rel="rel_sale_order_blanket_group_done",
        col1="type_id",
        col2="group_id",
    )
    blanket_cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        rel="rel_sale_order_blanket_group_cancel",
        col1="type_id",
        col2="group_id",
    )
    blanket_restart_group_ids = fields.Many2many(
        string="Allowed to Restart",
        comodel_name="res.groups",
        rel="rel_sale_order_blanket_group_restart",
        col1="type_id",
        col2="group_id",
    )

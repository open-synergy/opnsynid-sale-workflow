# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class CanvasRoute(models.Model):
    _name = "canvas.route"
    _description = "Sale Canvas Route"

    name = fields.Char(
        string="Canvas Route",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    inbound_warehouse_id = fields.Many2one(
        string="Inbound Warehouse",
        comodel_name="stock.warehouse",
    )
    outbound_warehouse_id = fields.Many2one(
        string="Outbound Warehouse",
        comodel_name="stock.warehouse",
    )
    inbound_route_id = fields.Many2one(
        string="Inbound Route",
        comodel_name="stock.location.route",
    )
    outbound_route_id = fields.Many2one(
        string="Outbound Route",
        comodel_name="stock.location.route",
    )
    sale_line_route_id = fields.Many2one(
        string="Sale Line Route",
        comodel_name="stock.location.route",
    )
    canvas_confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm Canvas",
        comodel_name="res.groups",
        relation="rel_canvas_route_confirm_canvas_order",
        column1="route_id",
        column2="group_id",
    )
    canvas_done_grp_ids = fields.Many2many(
        string="Allow To Done Canvas",
        comodel_name="res.groups",
        relation="rel_canvas_route_done_canvas_order",
        column1="route_id",
        column2="group_id",
    )
    canvas_cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel Canvas",
        comodel_name="res.groups",
        relation="rel_canvas_route_cancel_canvas_order",
        column1="route_id",
        column2="group_id",
    )
    canvas_restart_validation_grp_ids = fields.Many2many(
        string="Allow To Restart Canvas Validation",
        comodel_name="res.groups",
        relation="rel_canvas_route_restart_validation_canvas_order",
        column1="route_id",
        column2="group_id",
    )
    canvas_restart_grp_ids = fields.Many2many(
        string="Allow To Restart Canvas",
        comodel_name="res.groups",
        relation="rel_canvas_route_restart_canvas_order",
        column1="route_id",
        column2="group_id",
    )

# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class CanvasType(models.Model):
    _name = "canvas.type"
    _description = "Sale Canvas Type"

    name = fields.Char(
        string="Canvas Type",
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
    allowed_salesperson_ids = fields.Many2many(
        string="Allowed Salesperson",
        comodel_name="res.users",
        relation="rel_canvas_type_2_res_users",
        column1="type_id",
        column2="user_id",
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelist",
        comodel_name="product.pricelist",
        relation="rel_canvas_type_2_product_pricelist",
        column1="type_id",
        column2="pricelist_id",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        relation="rel_canvas_type_2_product",
        column1="type_id",
        column2="product_id",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_canvas_type_2_product_categ",
        column1="type_id",
        column2="category_id",
    )
    allowed_route_ids = fields.Many2many(
        string="Allowed Routes",
        comodel_name="canvas.route",
        relation="rel_canvas_type_2_canvas_route",
        column1="type_id",
        column2="route_id",
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )

# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    @api.depends(
        "allowed_product_categ_ids",
        "allowed_product_ids",
        "allowed_product_ids.sale_ok")
    def _compute_all_allowed_product_ids(self):
        obj_product = self.env["product.product"]
        for so_type in self:
            products = so_type.allowed_product_ids
            category_ids = so_type.allowed_product_categ_ids.ids
            criteria = [
                ("categ_id", "in", category_ids),
                ("sale_ok", "=", True),
            ]
            products += obj_product.search(criteria)
            so_type.all_allowed_product_ids = products

    limit_product_selection = fields.Boolean(
        string="Limit Product Selection",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="rel_so_type_2_product_categ",
        column1="type_id",
        column2="product_categ_id",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Product",
        comodel_name="product.product",
        domain=[("sale_ok", "=", True)],
        relation="rel_so_type_2_product",
        col1="type_id",
        col2="product_id",
    )
    all_allowed_product_ids = fields.Many2many(
        string="Allowed Product",
        comodel_name="product.product",
        compute="_compute_all_allowed_product_ids",
        store=True,
    )

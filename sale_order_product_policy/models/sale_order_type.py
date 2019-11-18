# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

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

# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    limit_warehouse_selection = fields.Boolean(
        string="Limit Warehouse Selection",
    )
    allowed_warehouse_ids = fields.Many2many(
        string="Allowed Warehouse",
        comodel_name="stock.warehouse",
        relation="rel_so_type_2_warehouse",
        column1="type_id",
        column2="warehouse_id",
    )

# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    limit_price_change = fields.Boolean(
        string="Limit Price Change",
    )
    price_change_group_ids = fields.Many2many(
        string="Allowed to Change Price on Sales Order",
        comodel_name="res.groups",
        rel="rel_sale_order_price_change",
        col1="type_id",
        col2="group_id",
    )

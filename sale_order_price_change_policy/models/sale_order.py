# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_price_change_policy(self):
        user = self.env.user
        for sale_order in self:
            order_type = sale_order.type_id
            price_change_ok = True
            if order_type and \
                    order_type.limit_price_change:
                for group in order_type.price_change_group_ids:
                    if user in group.users:
                        price_change_ok = True
                        break
                    else:
                        price_change_ok = False
            sale_order.price_change_ok = price_change_ok

    price_change_ok = fields.Boolean(
        string="Can Change Price",
        compute="_compute_price_change_policy",
        store=False,
    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    @api.depends(
        "order_id",
        "order_id.price_change_ok",
    )
    def _compute_price_change_policy(self):
        for line in self:
            line.price_change_ok = line.order_id.price_change_ok

    @api.multi
    @api.depends(
        "price_unit",
    )
    def _compute_price_change(self):
        for line in self:
            line.function_price_unit = line.price_unit

    price_change_ok = fields.Boolean(
        string="Can Change Price",
        compute="_compute_price_change_policy",
        store=False,
    )
    function_price_unit = fields.Float(
        string="Price Unit",
        store=False,
        compute="_compute_price_change",
        readonly=True,
    )

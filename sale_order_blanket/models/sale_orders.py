# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    blanket_order_id = fields.Many2one(
        comodel_name="sale.order.blanket",
        string="Origin blanket order",
        related="order_line.blanket_order_line.order_id",
        readonly=True,
    )

    @api.model
    def _check_exchausted_blanket_order_line(self):
        return any(
            line.blanket_order_line.remaining_qty < 0.0 for line in self.order_line
        )

    @api.multi
    def button_confirm(self):
        res = super(SaleOrder, self).button_confirm()
        for order in self:
            if order._check_exchausted_blanket_order_line():
                raise UserError(
                    _(
                        "Cannot confirm order %s as one of the lines refers "
                        "to a blanket order that has no remaining quantity."
                    )
                    % order.name
                )
        return res

    @api.constrains("partner_id")
    def check_partner_id(self):
        for line in self.order_line:
            if line.blanket_order_line:
                if line.blanket_order_line.partner_id != self.partner_id:
                    raise UserError(
                        _(
                            "The customer must be equal to the "
                            "blanket order lines customer"
                        )
                    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    blanket_order_line = fields.Many2one(
        comodel_name="sale.order.blanket.line",
        string="Blanket Order line",
        copy=False,
    )
    blanket_order_id = fields.Many2one(
        related="blanket_order_line.order_id",
    )

    @api.constrains("product_id")
    def check_product_id(self):
        if (
            self.blanket_order_line
            and self.product_id != self.blanket_order_line.product_id
        ):
            raise UserError(
                _(
                    "The product in the blanket order and in the "
                    "sales order must match"
                )
            )

    @api.constrains("currency_id")
    def check_currency(self):
        for line in self:
            if line.blanket_order_line:
                if line.currency_id != line.blanket_order_line.order_id.currency_id:
                    raise UserError(
                        _(
                            "The currency of the blanket order must match with "
                            "that of the sale order."
                        )
                    )

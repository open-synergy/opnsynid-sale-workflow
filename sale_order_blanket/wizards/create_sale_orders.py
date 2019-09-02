# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, _
from openerp.tools import float_is_zero
from collections import defaultdict
from openerp.exceptions import Warning as UserError


class SaleOrderBlanketWizard(models.TransientModel):
    _name = "sale.order.blanket.wizard"
    _description = "Blanket Order Wizard"

    @api.model
    def _default_order(self):
        if not self.env.context.get("active_id"):
            return False
        blanket_order = self.env["sale.order.blanket"].search(
            [("id", "=", self.env.context["active_id"])], limit=1)
        if blanket_order.state == "expired":
            raise UserError(_("You can\"t create a sale order from "
                              "an expired blanket order!"))
        return blanket_order

    @api.model
    def _check_valid_blanket_order_line(self, bo_lines):
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure")
        company_id = False
        list_currency_id = []
        list_pricelist_id = []
        list_user_id = []
        list_payment_term_id = []
        list_type_id = []

        if not bo_lines:
            raise UserError(_("An order can\"t be empty"))

        for line in bo_lines:
            if line.order_id.currency_id.id:
                list_currency_id.append(line.order_id.currency_id.id)
            if line.order_id.type_id.id:
                list_type_id.append(line.order_id.type_id.id)
            if line.order_id.pricelist_id.id:
                list_pricelist_id.append(line.order_id.pricelist_id.id)
            if line.order_id.user_id.id:
                list_user_id.append(line.order_id.user_id.id)
            if line.order_id.payment_term_id.id:
                list_payment_term_id.append(line.order_id.payment_term_id.id)

            if line.order_id.state != "open":
                raise UserError(
                    _("Sale Blanket Order %s is not open") %
                    line.order_id.name)

            if float_is_zero(
                    line.remaining_uom_qty, precision_digits=precision):
                raise UserError(
                    _("The sale has already been completed."))

            line_company_id = line.company_id and line.company_id.id or False
            if company_id is not False \
                    and line_company_id != company_id:
                raise UserError(
                    _("You have to select lines "
                      "from the same company."))
            else:
                company_id = line_company_id
        if list_currency_id and len(set(list_currency_id)) > 1:
            raise UserError(_("Can not create Sale Order from Blanket "
                              "Order lines with different currencies"))
        if list_type_id and len(set(list_type_id)) > 1:
            raise UserError(_("Can not create Sale Order from Blanket "
                              "Order lines with different order types"))
        if list_pricelist_id and len(set(list_pricelist_id)) > 1:
            raise UserError(_("Can not create Sale Order from Blanket "
                              "Order lines with different pricelist"))
        if list_payment_term_id and len(set(list_payment_term_id)) > 1:
            raise UserError(_("Can not create Sale Order from Blanket "
                              "Order lines with different payment term"))
        if list_user_id and len(set(list_user_id)) > 1:
            raise UserError(_("Can not create Sale Order from Blanket "
                              "Order lines with different user"))

    @api.model
    def _default_lines(self):
        blanket_order_line_obj = self.env["sale.order.blanket.line"]
        blanket_order_line_ids = self.env.context.get("active_ids", False)
        active_model = self.env.context.get("active_model", False)

        if active_model == "sale.order.blanket":
            bo_lines = self._default_order().line_ids
        else:
            bo_lines = blanket_order_line_obj.browse(blanket_order_line_ids)

        self._check_valid_blanket_order_line(bo_lines)

        lines = [(0, 0, self._prepare_order_line_data(l)) for l in bo_lines]

        return lines

    @api.multi
    def _prepare_order_line_data(self, line):
        result = {
            "blanket_line_id": line.id,
            "product_id": line.product_id.id,
            "date_schedule": line.date_schedule,
            "remaining_uom_qty": line.remaining_uom_qty,
            "price_unit": line.price_unit,
            "product_uom": line.product_uom.id,
            "qty": line.remaining_uom_qty,
            "partner_id": line.partner_id.id
        }
        return result

    blanket_order_id = fields.Many2one(
        comodel_name="sale.blanket.order",
        readonly=True
    )
    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale Order",
        domain=[("state", "=", "draft")]
    )
    line_ids = fields.One2many(
        comodel_name="sale.order.blanket.wizard.line",
        inverse_name="wizard_id",
        string="Lines",
        default=_default_lines
    )

    @api.multi
    def create_sale_order(self):
        order_lines = defaultdict(list)
        for line in self.line_ids:
            if line.qty == 0.0:
                continue

            if line.qty > line.remaining_uom_qty:
                raise UserError(
                    _("You can\"t order more than the remaining quantities"))

            vals = self._prepare_wizard_line_data(line)
            order_lines[line.partner_id.id].append((0, 0, vals))

        res = []
        for order_line in order_lines:
            order_vals =\
                self._prepare_sale_order_data(
                    order_line,
                    order_lines
                )
            sale_order = self.env["sale.order"].create(order_vals)
            res.append(sale_order.id)
        return {
            "domain": [("id", "in", res)],
            "name": _("Sales Orders"),
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "view_id": False,
            "context": {"from_sale_order": True},
            "type": "ir.actions.act_window"
        }

    @api.multi
    def _prepare_sale_order_data(
        self,
        order_line,
        order_lines
    ):
        self.ensure_one()

        vals = {
            "partner_id": order_line,
        }
        if self.blanket_order_id:
            vals.update({
                "origin": self.blanket_order_id.name,
                "user_id": self.blanket_order_id.user_id.id,
                "currency_id": self.blanket_order_id.currency_id.id,
                "pricelist_id": self.blanket_order_id.pricelist_id.id,
                "payment_term_id": self.blanket_order_id.payment_term_id.id,
            })
        vals.update({
            "order_line": order_lines[order_line],
        })
        return vals

    @api.multi
    def _prepare_wizard_line_data(self, line):
        self.ensure_one()
        result = {
            "product_id": line.product_id.id,
            "name": line.product_id.name,
            "product_uom": line.product_uom.id,
            "sequence": line.blanket_line_id.sequence,
            "price_unit": line.blanket_line_id.price_unit,
            "blanket_order_line": line.blanket_line_id.id,
            "product_uom_qty": line.qty,
            "tax_id": [(6, 0, line.taxes_id.ids)]
        }
        return result


class SaleOrderBlanketWizardLine(models.TransientModel):
    _name = "sale.order.blanket.wizard.line"

    wizard_id = fields.Many2one(
        comodel_name="sale.order.blanket.wizard"
    )
    blanket_line_id = fields.Many2one(
        comodel_name="sale.order.blanket.line"
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        related="blanket_line_id.product_id",
        string="Product",
        readonly=True
    )
    product_uom = fields.Many2one(
        comodel_name="product.uom",
        related="blanket_line_id.product_uom",
        string="Unit of Measure",
        readonly=True
    )
    date_schedule = fields.Date(
        related="blanket_line_id.date_schedule",
        readonly=True
    )
    remaining_uom_qty = fields.Float(
        related="blanket_line_id.remaining_uom_qty",
        readonly=True
    )
    qty = fields.Float(
        string="Quantity to Order",
        required=True
    )
    price_unit = fields.Float(
        related="blanket_line_id.price_unit",
        readonly=True
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="blanket_line_id.currency_id"
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="blanket_line_id.partner_id",
        string="Vendor",
        readonly=True,
    )
    taxes_id = fields.Many2many(
        comodel_name="account.tax",
        related="blanket_line_id.taxes_id",
        readonly=True
    )

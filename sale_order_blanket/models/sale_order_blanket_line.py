# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, SUPERUSER_ID, api, _
from openerp.exceptions import Warning as UserError
import openerp.addons.decimal_precision as dp
from openerp.tools import float_is_zero


class SaleOrderBlanketLine(models.Model):
    _name = "sale.order.blanket.line"
    _description = "Blanket Order Line"
    _inherit = [
        "mail.thread"
    ]

    @api.multi
    @api.depends(
        "original_uom_qty",
        "price_unit",
        "taxes_id",
        "order_id.partner_id",
        "product_id",
        "currency_id"
    )
    def _compute_amount(self):
        for line in self:
            price = line.price_unit
            taxes = line.taxes_id.compute_all(
                price,
                line.original_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_id
            )
            line.update({
                "price_tax": sum(
                    t.get("amount", 0.0) for t in taxes.get("taxes", [])),
                "price_total": taxes["total_included"],
                "price_subtotal": taxes["total"],
            })

    name = fields.Char(
        string="Description",
        track_visibility="onchange",
    )
    sequence = fields.Integer(
        string="Sequence",
    )
    order_id = fields.Many2one(
        string="# Blanket Order",
        comodel_name="sale.order.blanket",
        required=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        related="order_id.partner_id",
        store=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="sale.order.type",
        related="order_id.type_id",
        store=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        domain=[
            ("sale_ok", "=", True),
        ],
    )
    product_uom = fields.Many2one(
        string="Unit of Measure",
        comodel_name="product.uom",
        required=True,
    )
    price_unit = fields.Float(
        string="Price",
        required=True,
        digits=dp.get_precision("Product Price"),
    )
    taxes_id = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        domain=[
            "|",
            ("active", "=", False),
            ("active", "=", True),
        ],
    )
    taxes_id = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_blanket_order_line_taxes",
        column1="blanket_order_line_id",
        column2="tax_id",
    )
    date_schedule = fields.Date(
        string="Scheduled Date",
    )
    original_uom_qty = fields.Float(
        string="Original quantity",
        required=True,
        default=1,
        digits=dp.get_precision("Product Unit of Measure"),
    )
    ordered_uom_qty = fields.Float(
        string="Ordered quantity",
        compute="_compute_quantities",
        store=True,
    )
    invoiced_uom_qty = fields.Float(
        string="Invoiced quantity",
        compute="_compute_quantities",
        store=True,
    )
    remaining_uom_qty = fields.Float(
        string="Remaining quantity",
        compute="_compute_quantities",
        store=True,
    )
    remaining_qty = fields.Float(
        string="Remaining quantity in base UoM",
        compute="_compute_quantities",
        store=True,
    )
    delivered_uom_qty = fields.Float(
        string="Delivered quantity",
        compute="_compute_quantities",
        store=True,
    )
    sale_lines = fields.One2many(
        string="Sale order lines",
        comodel_name="sale.order.line",
        inverse_name="blanket_order_line",
        readonly=True,
        copy=False,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        related="order_id.company_id",
        store=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="order_id.currency_id",
        readonly=True,
    )
    partner_id = fields.Many2one(
        related="order_id.partner_id",
        string="Customer",
        readonly=True,
    )
    user_id = fields.Many2one(
        related="order_id.user_id",
        string="Responsible",
        readonly=True,
    )
    payment_term_id = fields.Many2one(
        related="order_id.payment_term_id",
        string="Payment Terms",
        readonly=True,
    )
    pricelist_id = fields.Many2one(
        related="order_id.pricelist_id",
        string="Pricelist",
        readonly=True,
    )
    price_subtotal = fields.Float(
        string="Subtotal",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_compute_amount",
    )
    price_total = fields.Float(
        string="Total",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_compute_amount",
    )
    price_tax = fields.Float(
        string="Tax",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_compute_amount",
    )

    @api.multi
    @api.onchange(
        "product_id"
    )
    def onchange_taxes_id(self):
        if self.product_id:
            fpos = self.order_id.fiscal_position_id
            if self.env.uid == SUPERUSER_ID:
                company_id = self.env.user.company_id.id
                self.taxes_id = fpos.map_tax(
                    self.product_id.supplier_taxes_id.filtered(
                        lambda r: r.company_id.id == company_id))
            else:
                self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id)

    @api.multi
    @api.onchange(
        "product_id"
    )
    def onchange_product_uom(self):
        if self.product_id:
            if not self.product_uom:
                self.product_uom = self.product_id.uom_id.id

    @api.multi
    @api.onchange(
        "product_id",
        "original_uom_qty"
    )
    def onchange_price_unit(self):
        obj_decimal_precision =\
            self.env["decimal.precision"]
        precision =\
            obj_decimal_precision.precision_get(
                "Product Unit of Measure")
        if self.product_id:
            if self.order_id.partner_id and \
                    float_is_zero(self.price_unit, precision_digits=precision):
                price = self.pricelist_id.price_get(
                    prod_id=self.product_id.id,
                    qty=self.original_uom_qty or 1.0
                )[self.pricelist_id.id]
                self.price_unit = price

    @api.multi
    @api.onchange(
        "product_id"
    )
    def onchange_name(self):
        if self.product_id:
            name = self.product_id.name
            if self.product_id.code:
                name = "[%s] %s" % (name, self.product_id.code)
            if self.product_id.description_sale:
                name += "\n" + self.product_id.description_sale
            self.name = name

    @api.multi
    @api.depends(
        "sale_lines.order_id.state",
        "sale_lines.blanket_order_line",
        "sale_lines.product_uom_qty",
        "sale_lines.product_uom",
        "sale_lines.invoice_lines",
        "sale_lines.procurement_ids",
        "original_uom_qty",
        "product_uom",
    )
    def _compute_quantities(self):
        for line in self:
            sale_lines = line.sale_lines
            ordered_uom_qty = 0.0
            invoiced_uom_qty = 0.0
            delivered_uom_qty = 0.0
            for l in sale_lines:
                if (
                    l.order_id.state != "cancel" and
                    l.product_id == line.product_id
                ):
                    ordered_uom_qty += l.product_uom._compute_qty(
                        line.product_uom, l.product_uom_qty)
                    if l.invoice_lines:
                        for inv in l.invoice_lines.filtered(
                            lambda r: r.invoice_id.state != "cancel"
                        ):
                            invoiced_uom_qty += inv.uos_id._compute_qty(
                                line.product_uom, inv.quantity)
                    if l.procurement_ids:
                        for proc in l.procurement_ids:
                            for move in proc.move_ids.filtered(
                                lambda r: r.state != "cancel"
                            ):
                                delivered_uom_qty +=\
                                    move.product_uom._compute_qty(
                                        line.product_uom, move.product_uom_qty)
            line.ordered_uom_qty = ordered_uom_qty
            line.invoiced_uom_qty = invoiced_uom_qty
            line.delivered_uom_qty = delivered_uom_qty
            line.remaining_uom_qty = line.original_uom_qty - \
                line.ordered_uom_qty
            line.remaining_qty = line.product_uom._compute_qty(
                line.product_id.uom_id, line.remaining_uom_qty)

    @api.multi
    def _validate(self):
        try:
            for line in self:
                assert line.price_unit > 0.0, \
                    _("Price must be greater than zero")
                assert line.original_uom_qty > 0.0, \
                    _("Quantity must be greater than zero")
        except AssertionError as e:
            raise UserError(e)

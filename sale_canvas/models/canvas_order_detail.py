# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class CanvasOrderDetail(models.Model):
    _name = "canvas.order_detail"
    _description = "Sale Canvas Order Detail"

    canvas_id = fields.Many2one(
        string="# Canvas",
        comodel_name="canvas.order",
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
    )

    @api.model
    def _default_pricelist_id(self):
        return self.env.context.get("pricelist_id", False)

    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
        default=lambda self: self._default_pricelist_id(),
    )
    quantity = fields.Float(
        string="Qty",
        required=True,
        default=1.0,
    )

    @api.depends(
        "product_id",
    )
    @api.multi
    def _compute_allowed_uom_ids(self):
        obj_uom = self.env["product.uom"]
        for document in self:
            result = []
            if document.product_id:
                categ = document.product_id.uom_id.category_id
                criteria = [
                    ("category_id", "=", categ.id),
                ]
                result = obj_uom.search(criteria).ids
            document.allowed_uom_ids = result

    allowed_uom_ids = fields.Many2many(
        string="Allowed UoM",
        comodel_name="product.uom",
        compute="_compute_allowed_uom_ids",
        store=False,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        required=True,
    )
    price_unit = fields.Float(
        string="Unit Price",
        required=True,
    )

    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_canvas_order_line_2_tax",
        column1="canvas_line_id",
        column2="tax_id",
    )

    @api.depends(
        "price_unit",
        "quantity",
        "tax_ids",
    )
    @api.multi
    def _compute_price(self):
        for document in self:
            subtotal_tax_comp = document.tax_ids.compute_all(
                price_unit=document.price_unit,
                quantity=document.quantity,
                product=document.product_id,
            )
            price_tax_comp = document.tax_ids.compute_all(
                price_unit=document.price_unit,
                quantity=1.0,
                product=document.product_id,
            )
            document.price_before_tax = price_tax_comp["total"]
            document.price_after_tax = price_tax_comp["total_included"]
            document.subtotal_before_tax = subtotal_tax_comp["total"]
            document.subtotal_after_tax = subtotal_tax_comp["total_included"]

    price_before_tax = fields.Float(
        string="Unit Price Before Tax",
        compute="_compute_price",
        store=True,
    )
    price_after_tax = fields.Float(
        string="Unit Price After Tax",
        compute="_compute_price",
        store=True,
    )
    subtotal_before_tax = fields.Float(
        string="Subtotal Before Tax",
        compute="_compute_price",
        store=True,
    )
    subtotal_after_tax = fields.Float(
        string="Subtotal Before Tax",
        compute="_compute_price",
        store=True,
    )
    outbound_stock_move_ids = fields.Many2many(
        string="Outbound Moves",
        comodel_name="stock.move",
        relation="rel_canvas_order_line_2_outbound_move",
        column1="canvas_line_id",
        column2="move_id",
        readonly="1",
    )

    @api.depends(
        "outbound_stock_move_ids",
        "outbound_stock_move_ids.state",
        "outbound_stock_move_ids.product_qty",
    )
    @api.multi
    def _compute_qty_deliver(self):
        for document in self:
            qty_delivered = 0.0
            for move in document.outbound_stock_move_ids:
                if move.state == "done":
                    qty_delivered += move.product_qty
            document.qty_delivered = qty_delivered
            document.qty_to_deliver = document.quantity - qty_delivered

    qty_to_deliver = fields.Float(
        string="Qty To Deliver",
        compute="_compute_qty_deliver",
        store=True,
    )
    qty_delivered = fields.Float(
        string="Qty Delivered",
        compute="_compute_qty_deliver",
        store=True,
    )

    inbound_stock_move_ids = fields.Many2many(
        string="Inbound Moves",
        comodel_name="stock.move",
        relation="rel_canvas_order_line_2_inbound_move",
        column1="canvas_line_id",
        column2="move_id",
        readonly="1",
    )

    @api.depends(
        "inbound_stock_move_ids",
        "inbound_stock_move_ids.state",
        "inbound_stock_move_ids.product_qty",
    )
    @api.multi
    def _compute_qty_receive(self):
        for document in self:
            qty_received = 0.0
            for move in document.inbound_stock_move_ids:
                if move.state == "done":
                    qty_received += move.product_qty
            document.qty_received = qty_received

    qty_received = fields.Float(
        string="Qty Received",
        compute="_compute_qty_receive",
        store=True,
    )

    @api.depends(
        "qty_delivered",
        "qty_sold",
        "qty_missing",
        "qty_waste",
    )
    @api.multi
    def _compute_qty_to_receive(self):
        for document in self:
            document.qty_to_receive = (
                document.qty_delivered
                - document.qty_sold
                - document.qty_missing
                - document.qty_waste
            )

    qty_to_receive = fields.Float(
        string="Qty To Receive",
        compute="_compute_qty_to_receive",
        store=True,
    )
    missing_stock_move_ids = fields.Many2many(
        string="Missing Moves",
        comodel_name="stock.move",
        relation="rel_canvas_order_line_2_missing_move",
        column1="canvas_line_id",
        column2="move_id",
        readonly="1",
    )

    @api.depends(
        "missing_stock_move_ids",
        "missing_stock_move_ids.state",
        "missing_stock_move_ids.product_qty",
    )
    @api.multi
    def _compute_qty_missing(self):
        for document in self:
            qty_missing = 0.0
            for move in document.missing_stock_move_ids:
                if move.state == "done":
                    qty_missing += move.product_qty
            document.qty_missing = qty_missing

    qty_missing = fields.Float(
        string="Qty Missing",
        compute="_compute_qty_missing",
        store=True,
    )
    waste_stock_move_ids = fields.Many2many(
        string="Waste Moves",
        comodel_name="stock.move",
        relation="rel_canvas_order_line_2_waste_move",
        column1="canvas_line_id",
        column2="move_id",
        readonly="1",
    )

    @api.depends(
        "waste_stock_move_ids",
        "waste_stock_move_ids.state",
        "waste_stock_move_ids.product_qty",
    )
    @api.multi
    def _compute_qty_waste(self):
        for document in self:
            qty_waste = 0.0
            for move in document.waste_stock_move_ids:
                if move.state == "done":
                    qty_waste += move.product_qty
            document.qty_waste = qty_waste

    qty_waste = fields.Float(
        string="Qty Waste",
        compute="_compute_qty_waste",
        store=True,
    )
    order_line_ids = fields.Many2many(
        string="Order Lines",
        comodel_name="sale.order.line",
        relation="rel_canvas_order_line_2_order_line",
        column1="canvas_line_id",
        column2="order_line_id",
        readonly="1",
    )

    @api.depends(
        "order_line_ids",
        "order_line_ids.state",
        "order_line_ids.product_uom_qty",
    )
    @api.multi
    def _compute_qty_sold(self):
        for document in self:
            qty_sold = 0.0
            for line in document.order_line_ids:
                if line.state in ["confirmed", "exception", "done"]:
                    qty_sold += line.product_uom_qty
            document.qty_sold = qty_sold

    qty_sold = fields.Float(
        string="Qty Sold",
        compute="_compute_qty_sold",
        store=True,
    )

    @api.onchange(
        "product_id",
    )
    def onchange_uom_id(self):
        self.uom_id = False
        if self.product_id:
            self.uom_id = self.product_id.uom_id

    @api.onchange(
        "product_id",
        "pricelist_id",
        "uom_id",
        "quantity",
    )
    def onchange_price_unit(self):
        obj_uom = self.env["product.uom"]
        price_unit = 0.0
        if self.pricelist_id and self.product_id and self.quantity:
            pricelist_id = self.pricelist_id.id
            price_unit = self.pricelist_id.price_get(
                prod_id=self.product_id.id, qty=self.quantity
            )[pricelist_id]
            if self.uom_id:
                price_unit = obj_uom._compute_price(
                    self.product_id.uom_id.id, price_unit, self.uom_id.id
                )
        self.price_unit = price_unit

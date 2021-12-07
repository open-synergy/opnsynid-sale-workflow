# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    @api.depends(
        "product_id",
    )
    def _compute_require_packaging_on_sale(self):
        for line in self:
            line.require_packaging_on_sale = line.product_id.require_packaging_on_sale

    require_packaging_on_sale = fields.Boolean(
        string="Require Packaging on Sale",
        compute="_compute_require_packaging_on_sale",
    )

    @api.constrains(
        "product_id",
        "product_packaging",
        "product_uom_qty",
        "product_uom",
    )
    def _check_packaging(self):
        obj_uom = self.env["product.uom"]
        if self.product_packaging:
            default_uom_id = self.product_id.uom_id and self.product_id.uom_id.id
            pack = self.product_packaging
            q = obj_uom._compute_qty(self.product_uom.id, pack.qty, default_uom_id)
            if self.product_uom_qty and (q and not (self.product_uom_qty % q) == 0):
                # TODO: Decent error message
                msg = _("Unmatch qty with packaging in one of the lines")
                raise UserError(msg)

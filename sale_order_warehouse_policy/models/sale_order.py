# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends(
        "type_id",
        "type_id.allowed_warehouse_ids")
    def _compute_allowed_warehouse_ids(self):
        obj_wh = self.env["stock.warehouse"]
        for so in self:
            if so.type_id.limit_warehouse_selection:
                so.allowed_warehouse_ids = \
                    so.type_id.allowed_warehouse_ids
            else:
                criteria = []
                so.allowed_warehouse_ids = \
                    obj_wh.search(criteria)

    allowed_warehouse_ids = fields.Many2many(
        string="Allowed Warehouse",
        comodel_name="stock.warehouse",
        compute="_compute_allowed_warehouse_ids",
        store=False,
    )

    @api.onchange("type_id")
    def onchange_type_id(self):
        super(SaleOrder, self).onchange_type_id()
        if self.allowed_warehouse_ids:
            self.warehouse_id = self.allowed_warehouse_ids[0]

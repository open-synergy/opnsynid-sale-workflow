# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends(
        "type_id",
        "type_id.all_allowed_product_ids",
    )
    def _compute_all_allowed_product_ids(self):
        obj_product = self.env["product.product"]
        for so in self:
            if so.type_id.limit_product_selection:
                so.all_allowed_product_ids = \
                    so.type_id.all_allowed_product_ids
            else:
                criteria = [
                    ("sale_ok", "=", True),
                ]
                so.all_allowed_product_ids = \
                    obj_product.search(criteria)

    all_allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        compute="_compute_all_allowed_product_ids",
        store=False,
    )

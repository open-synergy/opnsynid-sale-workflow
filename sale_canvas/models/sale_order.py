# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    canvas_id = fields.Many2one(
        string="# Canvas",
        comodel_name="canvas.order",
        ondelete="cascade",
    )

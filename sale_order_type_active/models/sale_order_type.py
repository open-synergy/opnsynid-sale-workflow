# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class SaleOrderType(models.Model):
    _name = "sale.order.type"
    _inherit = "sale.order.type"

    active = fields.Boolean(
        string="Active",
        default=True,
    )

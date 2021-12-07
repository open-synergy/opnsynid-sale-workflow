# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    auto_create_contract = fields.Boolean(
        string="Auto Create Contract",
        default=False,
    )

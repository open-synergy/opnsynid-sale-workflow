# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResPartnerPricelistType(models.Model):
    _name = "res.partner_pricelist_type"

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner"
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        domain=[('type', '=', 'sale')],
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="sale.order.type"
    )

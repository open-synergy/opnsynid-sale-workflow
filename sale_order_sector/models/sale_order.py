# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    primary_sector_id = fields.Many2one(
        string="Primary Sector",
        comodel_name="res.partner.sector",
        related="partner_id.commercial_partner_id.sector_id",
        store=True,
        readonly=True,
    )

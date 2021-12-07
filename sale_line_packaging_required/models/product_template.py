# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    require_packaging_on_sale = fields.Boolean(
        string="Require Packaging on Sale",
    )

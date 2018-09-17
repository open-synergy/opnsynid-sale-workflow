# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    pricelist_by_type_ids = fields.One2many(
        string="Pricelist By Type",
        comodel_name="res.partner_pricelist_type",
        inverse_name="partner_id",
    )

    @api.model
    def get_pricelist_by_type(self, order_type):
        result = False
        obj_partner_pricelist_type =\
            self.env["res.partner_pricelist_type"]
        criteria = [
            ("partner_id", "=", self.id),
            ("type_id", "=", order_type.id)
        ]
        pricelist =\
            obj_partner_pricelist_type.search(criteria)
        if pricelist:
            result = pricelist.pricelist_id
        return result

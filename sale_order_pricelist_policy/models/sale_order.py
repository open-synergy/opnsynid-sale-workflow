# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_id")
    def new_onchange_pricelist_id(self):
        order_type = self.type_id
        if self.partner_id.parent_id:
            partner = self.partner_id.parent_id
        else:
            partner = self.partner_id
        _super = super(SaleOrder, self)
        old_res =\
            _super.onchange_partner_id(self.partner_id.id)
        if type(old_res) is dict and "value" in old_res:
            for field, value in old_res.get("value").items():
                if hasattr(self, field):
                    setattr(self, field, value)
        if order_type:
            pricelist =\
                partner.get_pricelist_by_type(order_type)
            if pricelist:
                self.type_id = order_type
                self.pricelist_id = pricelist

    @api.onchange("type_id")
    def onchange_type_id(self):
        _super = super(SaleOrder, self)
        res = _super.onchange_type_id()
        if self.partner_id.parent_id:
            partner = self.partner_id.parent_id
        else:
            partner = self.partner_id
        type_id = self.type_id

        if partner:
            pricelist =\
                partner.get_pricelist_by_type(type_id)
            if pricelist:
                self.pricelist_id = pricelist
            else:
                return res
        else:
            return res

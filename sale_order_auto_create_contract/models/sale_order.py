# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    @api.multi
    def action_button_confirm(self):
        _super = super(SaleOrder, self)
        _super.action_button_confirm()
        for sale in self:
            sale._assign_contract()
        return True

    @api.multi
    def _assign_contract(self):
        self.ensure_one()
        contract = self._create_contract()
        if contract:
            self.write({"project_id": contract.id})

    @api.multi
    def _create_contract(self):
        self.ensure_one()
        result = False
        if self.type_id and \
                self.type_id.auto_create_contract and \
                not self.project_id:
            obj_contract = self.env["account.analytic.account"]
            result = obj_contract.create(self._prepare_contract())
        return result

    @api.multi
    def _prepare_contract(self):
        self.ensure_one()
        name = self.client_order_ref or self.name
        return {
            "name": name,
            "type": "contract",
            "partner_id": self.partner_id.commercial_partner_id.id,
            "manager_id": self.user_id.id,
        }

# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    @api.multi
    def action_wait(self):
        _super = super(SaleOrder, self)
        _super.action_wait()
        for sale in self:
            contract = sale._create_contract()
            contract_id = contract and contract.id or False
            sale.write({"project_id": contract_id})
        return True

    @api.multi
    def _create_contract(self):
        self.ensure_one()
        obj_contract = self.env["account.analytic.account"]
        return obj_contract.create(self._prepare_contract())

    @api.multi
    def _prepare_contract(self):
        self.ensure_one()
        name = self.client_order_ref or self.name
        return {
            "name": name,
            "type": "contract",
            "partner_id": self.partner_id.commercial_partner_id.id,
            "code": self.name,
            "manager_id": self.user_id.id,
        }

# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    @api.multi
    def _create_contract(self):
        self.ensure_one()
        _super = super(SaleOrder, self)
        result = False
        if (
            self.type_id
            and self.type_id.auto_create_project
            and self.type_id.project_template_id
            and not self.project_id
        ):
            project_name = self.client_order_ref or self.name
            project = self.type_id.project_template_id._create_project(
                project_name=project_name,
                partner_id=self.partner_id.commercial_partner_id.id,
            )
            result = project.analytic_account_id
        elif self.type_id and self.type_id.auto_create_contract and not self.project_id:
            result = _super._create_contract()
        return result

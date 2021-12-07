# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    auto_create_project = fields.Boolean(
        string="Auto Create Project",
        default=False,
    )
    project_template_id = fields.Many2one(
        string="Project Template",
        comodel_name="project.template",
    )

    @api.onchange(
        "auto_create_project",
    )
    def onchange_auto_create_contract(self):
        if self.auto_create_project:
            self.auto_create_contract = True

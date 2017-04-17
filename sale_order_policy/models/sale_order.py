# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    @api.depends(
        "state",
        "type_id.invoice_recreate_group_ids",
        "type_id.invoice_corrected_group_ids",
        "type_id.quotation_send_group_ids",
        "type_id.confirm_order_group_ids",
        "type_id.view_invoice_group_ids",
        "type_id.create_invoice_group_ids",
        "type_id.copy_quotation_group_ids",
        "type_id.cancel_quot_group_ids",
        "type_id.cancel_order_group_ids"
    )
    def _compute_policy(self):
        user_id = self.env.user.id
        for sale_order in self:
            order_type = sale_order.type_id
            if user_id == SUPERUSER_ID or not order_type:
                sale_order.invoice_recreate_ok = True
                sale_order.invoice_corrected_ok = True
                sale_order.quotation_send_ok = True
                sale_order.confirm_order_ok = True
                sale_order.view_invoice_ok = True
                sale_order.create_invoice_ok = True
                sale_order.copy_quotation_ok = True
                sale_order.cancel_quot_ok = True
                sale_order.cancel_order_ok = True
                continue

            sale_order.invoice_recreate_ok =\
                self._button_policy(order_type, 'invoice_recreate')
            sale_order.invoice_corrected_ok =\
                self._button_policy(order_type, 'invoice_corrected')
            sale_order.quotation_send_ok =\
                self._button_policy(order_type, 'quotation_send')
            sale_order.confirm_order_ok =\
                self._button_policy(order_type, 'confirm_order')
            sale_order.view_invoice_ok =\
                self._button_policy(order_type, 'view_invoice')
            sale_order.create_invoice_ok =\
                self._button_policy(order_type, 'create_invoice')
            sale_order.copy_quotation_ok =\
                self._button_policy(order_type, 'copy_quotation')
            sale_order.cancel_quot_ok =\
                self._button_policy(order_type, 'cancel_quot')
            sale_order.cancel_order_ok =\
                self._button_policy(order_type, 'cancel_order')

    @api.model
    def _button_policy(self, order_type, button_type):
        user = self.env.user
        group_ids = user.groups_id.ids
        button_group_ids = []

        if button_type == 'invoice_recreate':
            button_group_ids = order_type.invoice_recreate_group_ids.ids
        elif button_type == 'invoice_corrected':
            button_group_ids = order_type.invoice_corrected_group_ids.ids
        elif button_type == 'quotation_send':
            button_group_ids = order_type.quotation_send_group_ids.ids
        elif button_type == 'confirm_order':
            button_group_ids = order_type.confirm_order_group_ids.ids
        elif button_type == 'view_invoice':
            button_group_ids = order_type.view_invoice_group_ids.ids
        elif button_type == 'create_invoice':
            button_group_ids = order_type.create_invoice_group_ids.ids
        elif button_type == 'copy_quotation':
            button_group_ids = order_type.copy_quotation_group_ids.ids
        elif button_type == 'cancel_quot':
            button_group_ids = order_type.cancel_quot_group_ids.ids
        elif button_type == 'cancel_order':
            button_group_ids = order_type.cancel_order_group_ids.ids

        if button_group_ids:
            if (set(button_group_ids) & set(group_ids)):
                result = True
            else:
                result = False
        else:
            result = True
        return result

    invoice_recreate_ok = fields.Boolean(
        string="Can Recreate Invoice",
        compute="_compute_policy",
        store=False,
    )
    invoice_corrected_ok = fields.Boolean(
        string="Can Ignore Exception",
        compute="_compute_policy",
        store=False,
    )
    quotation_send_ok = fields.Boolean(
        string="Can Send by Email",
        compute="_compute_policy",
        store=False,
    )
    confirm_order_ok = fields.Boolean(
        string="Can Confirm Sale",
        compute="_compute_policy",
        store=False,
    )
    view_invoice_ok = fields.Boolean(
        string="Can View Invoice",
        compute="_compute_policy",
        store=False,
    )
    create_invoice_ok = fields.Boolean(
        string="Can Create Invoice",
        compute="_compute_policy",
        store=False,
    )
    copy_quotation_ok = fields.Boolean(
        string="Can New Copy of Quotation",
        compute="_compute_policy",
        store=False,
    )
    cancel_quot_ok = fields.Boolean(
        string="Can Cancel Quotation",
        compute="_compute_policy",
        store=False,
    )
    cancel_order_ok = fields.Boolean(
        string="Can Cancel Order",
        compute="_compute_policy",
        store=False,
    )

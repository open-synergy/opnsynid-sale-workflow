# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError
import openerp.addons.decimal_precision as dp


class SaleOrderBlanket(models.Model):
    _name = "sale.order.blanket"
    _description = "Blanket Orders"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.document_version",
        "base.cancel.reason_common"
    ]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id

    @api.multi
    @api.depends(
        "type_id",
    )
    def _compute_policy(self):
        _super = super(SaleOrderBlanket, self)
        _super._compute_policy()

    @api.depends("line_ids.price_total")
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.line_ids:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                "amount_untaxed": order.currency_id.round(amount_untaxed),
                "amount_tax": order.currency_id.round(amount_tax),
                "amount_total": amount_untaxed + amount_tax,
            })

    name = fields.Char(
        string="Name",
        required=True,
        default="/",
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    payment_term_id = fields.Many2one(
        string="Payment Terms",
        comodel_name="account.payment.term",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.model
    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="pricelist_id.currency_id",
        store=True,
        readonly=True,
        default=lambda self: self._default_currency_id(),
    )

    @api.model
    def _get_order_type(self):
        return self.env["sale.order.type"].search([])[:1].id

    type_id = fields.Many2one(
        comodel_name="sale.order.type",
        string="Type",
        default=lambda self: self._get_order_type(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )

    validity_date = fields.Date(
        string="Validity Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    user_id = fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    fiscal_position_id = fields.Many2one(
        string="Fiscal Position",
        comodel_name="account.fiscal.position"
    )

    @api.model
    def _get_default_section_id(self):
        """ Gives default section by checking if present in the context """
        obj_res_users = self.env["res.users"]
        context = self._context
        section_id = \
            self.with_context(
                context
            )._resolve_section_id_from_context() or False
        if not section_id:
            section_id =\
                obj_res_users.with_context(
                    context
                ).browse(
                    self.env.user.id
                ).default_section_id.id or False
        return section_id

    @api.model
    def _resolve_section_id_from_context(self):
        """ Returns ID of section based on the value of "section_id"
            context key, or None if it cannot be resolved to a single
            Sales Team.
        """
        context = self._context
        obj_section = self.env["crm.case.section"]
        if type(context.get("default_section_id")) in (int, long):
            return context.get("default_section_id")
        if isinstance(context.get("default_section_id"), basestring):
            section_ids =\
                obj_section.with_context(
                    context
                ).name_search(
                    name=context["default_section_id"]
                )
            if len(section_ids) == 1:
                return int(section_ids[0][0])
        return None

    section_id = fields.Many2one(
        string="Sales Team",
        comodel_name="crm.case.section",
        change_default=True,
        default=lambda self: self._get_default_section_id(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    client_order_ref = fields.Char(
        string="Customer Reference",
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    line_ids = fields.One2many(
        string="Order lines",
        comodel_name="sale.order.blanket.line",
        inverse_name="order_id",
        copy=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_untaxed = fields.Float(
        string="Untaxed Amount",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_amount_all",
    )
    amount_tax = fields.Float(
        string="Taxes",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_amount_all",
    )
    amount_total = fields.Float(
        string="Total",
        digits=dp.get_precision("Account"),
        store=True,
        readonly=True,
        compute="_amount_all",
    )
    line_count = fields.Integer(
        string="Sale Blanket Order Line count",
        compute="_compute_line_count",
        readonly=True,
    )

    @api.depends("line_ids")
    def _compute_line_count(self):
        self.line_count = len(self.mapped("line_ids"))

    sale_count = fields.Integer(
        string="Sale Count",
        compute="_compute_sale_count",
    )

    @api.multi
    def _get_sale_orders(self):
        return self.mapped("line_ids.sale_lines.order_id")

    @api.multi
    def _compute_sale_count(self):
        for blanket_order in self:
            blanket_order.sale_count = len(blanket_order._get_sale_orders())

    state = fields.Selection(
        string="State",
        copy=False,
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "On Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        required=True,
        readonly=True,
        default="draft",
    )
    note = fields.Text(
        string="Note",
    )

    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    open_date = fields.Datetime(
        string="Opened Date",
        readonly=True,
        copy=False,
    )
    open_user_id = fields.Many2one(
        string="Opened By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    done_date = fields.Datetime(
        string="Done Date",
        readonly=True,
        copy=False,
    )
    done_user_id = fields.Many2one(
        string="Done By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancellation Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancellation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )

    # Policy Fields
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    open_ok = fields.Boolean(
        string="Can Open",
        compute="_compute_policy",
    )
    done_ok = fields.Boolean(
        string="Can Finish",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )

    @api.multi
    @api.onchange(
        "partner_id"
    )
    def onchange_user_id(self):
        if not self.partner_id:
            self.user_id = False
            return

        self.user_id = (
            self.partner_id.user_id and
            self.partner_id.user_id.id or
            False
        )

    @api.multi
    @api.onchange(
        "partner_id",
        "company_id"
    )
    def onchange_fiscal_position_id(self):
        if not self.partner_id:
            self.fiscal_position_id = False
            return

        obj_fiscal_position =\
            self.env["account.fiscal.position"]
        self.fiscal_position_id =\
            obj_fiscal_position.get_fiscal_position(
                self.company_id.id,
                self.partner_id.id
            )

    @api.multi
    @api.onchange(
        "partner_id"
    )
    def onchange_payment_term_id(self):
        if not self.partner_id:
            self.payment_term_id = False
            return

        obj_res_partner =\
            self.env["res.partner"]
        partner = obj_res_partner.browse(self.partner_id.id)
        addr = partner.address_get(["invoice"])
        invoice_part = obj_res_partner.browse(addr["invoice"])
        self.payment_term_id = (
            invoice_part.property_payment_term and
            invoice_part.property_payment_term.id or
            False
        )

    @api.multi
    @api.onchange(
        "partner_id"
    )
    def onchange_pricelist_id(self):
        if not self.partner_id:
            self.pricelist_id = False
            return
        self.pricelist_id = (
            self.partner_id.property_product_pricelist and
            self.partner_id.property_product_pricelist.id or
            False
        )

    @api.multi
    def action_view_sale_orders(self):
        sale_orders = self._get_sale_orders()
        action = self.env.ref('sale.action_orders').read()[0]
        if len(sale_orders) > 0:
            action['domain'] = [('id', 'in', sale_orders.ids)]
            action['context'] = [('id', 'in', sale_orders.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_view_sale_blanket_order_line(self):
        action = self.env.ref(
            'sale_order_blanket'
            '.sale_order_blanket_line_action').read()[0]
        lines = self.mapped('line_ids')
        if len(lines) > 0:
            action['domain'] = [('id', 'in', lines.ids)]
        return action

    @api.model
    def create(self, values):
        _super = super(SaleOrderBlanket, self)
        result = _super.create(values)
        sequence = result._create_sequence()
        result.write({
            "name": sequence,
        })
        return result

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(SaleOrderBlanket, self)
        _super.unlink()

    @api.multi
    def button_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())

    @api.multi
    def button_open(self):
        for document in self:
            document.write(document._prepare_open_data())

    @api.multi
    def button_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    @api.multi
    def button_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())

    @api.multi
    def button_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        result = {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_open_data(self):
        self.ensure_one()
        result = {
            "state": "open",
            "open_date": fields.Datetime.now(),
            "open_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        result = {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
        }
        return result

    @api.model
    def _prepare_cancel_data(self):
        result = {
            "state": "cancel",
            "cancelled_date": fields.Datetime.now(),
            "cancelled_user_id": self.env.user.id,
            "cancel_reason_id": self.cancel_reason_id,
            "signed_document_id": False,
        }
        return result

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        result = {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "open_date": False,
            "open_user_id": False,
            "done_date": False,
            "done_user_id": False,
        }
        return result

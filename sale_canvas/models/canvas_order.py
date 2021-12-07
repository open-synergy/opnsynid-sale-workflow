# -*- coding: utf-8 -*-
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class CanvasOrder(models.Model):
    _name = "canvas.order"
    _description = "Sale Canvas Order"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["approve"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.multi
    def _compute_policy(self):
        _super = super(CanvasOrder, self)
        _super._compute_policy()

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
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
    date_order = fields.Date(
        string="Date Order",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    salesperson_id = fields.Many2one(
        string="Sales Person",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="canvas.type",
        required=True,
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
    route_id = fields.Many2one(
        string="Route",
        comodel_name="canvas.route",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    sale_ids = fields.One2many(
        string="Sales",
        comodel_name="sale.order",
        inverse_name="canvas_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="canvas.order_detail",
        inverse_name="canvas_id",
        copy=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_salesperson_ids = fields.Many2many(
        string="Allowed Salesperson",
        comodel_name="res.users",
        related="type_id.allowed_salesperson_ids",
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelist",
        comodel_name="product.pricelist",
        related="type_id.allowed_pricelist_ids",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        related="type_id.allowed_product_categ_ids",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        related="type_id.allowed_product_ids",
    )
    allowed_route_ids = fields.Many2many(
        string="Allowed Routes",
        comodel_name="canvas.route",
        related="type_id.allowed_route_ids",
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Approved"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirm Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    approve_date = fields.Datetime(
        string="Approve Date",
        readonly=True,
        copy=False,
    )
    approve_user_id = fields.Many2one(
        string="Approve By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    done_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
        copy=False,
    )
    done_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )

    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    done_ok = fields.Boolean(
        string="Can Done",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_validation_ok = fields.Boolean(
        string="Can Restart Validation",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())
            document.request_validation()

    @api.multi
    def action_approve(self):
        for document in self:
            document.write(document._prepare_approve_data())
            if not document.move_id:
                document._create_accounting_entry()

    @api.multi
    def action_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    @api.multi
    def action_cancel(self):
        for document in self:
            move = document.move_id
            document.write(document._prepare_cancel_data())
            if move:
                move.unlink()
            document.restart_validation()

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_approve_data(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update(
            {
                "ir_sequence_date": self.date_expense,
            }
        )
        sequence = self.with_context(ctx)._create_sequence()
        return {
            "state": "approve",
            "name": sequence,
            "approve_date": fields.Datetime.now(),
            "approve_user_id": self.env.user.id,
            "done_date": False,
            "done_user_id": False,
        }

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        return {
            "state": "done",
            "done_date": fields.Datetime.now(),
            "done_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "approve_date": False,
            "approve_user_id": False,
            "done_date": False,
            "done_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
            "terminate_date": False,
            "terminate_user_id": False,
            "cancel_reason_id": False,
            "terminate_reason_id": False,
        }

    @api.onchange(
        "type_id",
    )
    def onchange_salesperson_id(self):
        self.salesperson_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_route_id(self):
        self.route_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(CanvasOrder, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(CanvasOrder, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_approve()

    @api.multi
    def restart_validation(self):
        _super = super(CanvasOrder, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

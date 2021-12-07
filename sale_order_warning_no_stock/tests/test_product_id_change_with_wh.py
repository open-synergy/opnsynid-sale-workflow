# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductIdChangeWithWh(TransactionCase):
    def setUp(self):
        super(TestProductIdChangeWithWh, self).setUp()

        # Object
        self.obj_sale_order = self.env["sale.order"]
        self.obj_sale_order_line = self.env["sale.order.line"]

        # Data
        self.partner = self.env.ref("base.res_partner_1")
        self.product = self.env.ref("product.product_product_14")

    def test_product_id_change_with_wh(self):
        self.order = self.obj_sale_order.create(
            {
                "partner_id": self.partner.id,
            }
        )
        self.order_line = self.obj_sale_order_line.create(
            {
                "name": "Test Line",
                "order_id": self.order.id,
                "product_id": self.product.id,
                "product_uom_qty": 1000,
            }
        )

        onchange_res = self.registry("sale.order.line").product_id_change_with_wh(
            self.cr,
            self.uid,
            [],
            self.order.pricelist_id.id,
            self.order_line.product_id.id,
            qty=self.order_line.product_uom_qty,
            uom=self.order_line.product_uom.id,
            qty_uos=0,
            uos=False,
            name="",
            partner_id=self.order.partner_id.id,
            lang=False,
            update_tax=True,
            date_order=self.order.date_order,
            packaging=False,
            fiscal_position=False,
            flag=False,
            warehouse_id=self.order.warehouse_id.id,
            context=self.env.context,
        )
        self.assertEqual(onchange_res["warning"], {})

# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestOnchangeProductBarcode(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestOnchangeProductBarcode, self).setUp(*args, **kwargs)
        # Objects
        self.wiz = self.env['sale.order.barcode']
        self.obj_sale_order_line =\
            self.env['sale.order.line']

        # Data
        self.data_so = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        self.product_1 =\
            self.env.ref('product.product_product_25')
        self.product_2 =\
            self.env.ref('product.product_product_30')
        self.product_3 =\
            self.env.ref('product.product_product_3')

    def test_product_barcode_change_1(self):
        new = self.wiz.with_context(
            active_model="sale.order",
            active_id=self.data_so.id
        ).new()

        new.product_barcode = 0000000000000
        res = new.product_barcode_change()
        self.assertEquals(
            'No product found with this code as '
            'EAN13 or product is not for sale. You should select '
            'the right product manually.',
            res['warning']['message']
        )

        self.product_1.ean13 = 8998989300155
        self.product_2.ean13 = 8998989300155

        new.product_barcode = 8998989300155
        res = new.product_barcode_change()
        self.assertIsNotNone(
            res['warning']['message']
        )

    def test_product_barcode_change_2(self):
        self.product_1.ean13 = 8998989300155
        self.product_2.ean13 = 8996001600382
        self.product_3.ean13 = 8998666000903

        new = self.wiz.with_context(
            active_model="sale.order",
            active_id=self.data_so.id
        ).new()

        new.product_barcode = 8998989300155
        new.product_barcode_change()
        new.product_barcode = 8998989300155
        new.product_barcode_change()
        line_1 = self.obj_sale_order_line.search([
            ('order_id', '=', self.data_so.id),
            ('product_id', '=', self.product_1.id)
        ])
        self.assertEqual(line_1.product_uom_qty, 2.0)

        new.product_barcode = 8996001600382
        new.product_barcode_change()
        line_2 = self.obj_sale_order_line.search([
            ('order_id', '=', self.data_so.id),
            ('product_id', '=', self.product_2.id)
        ])
        self.assertEqual(line_2.product_uom_qty, 1.0)

        new.product_barcode = 8998666000903
        new.product_barcode_change()
        line_3 = self.obj_sale_order_line.search([
            ('order_id', '=', self.data_so.id),
            ('product_id', '=', self.product_3.id)
        ])
        self.assertEqual(line_3.product_uom_qty, 1.0)

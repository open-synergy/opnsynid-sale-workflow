# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _


class SaleOrderBarcode(models.TransientModel):
    _name = 'sale.order.barcode'
    _description = 'Sale Order Barcode Wizard'

    product_barcode = fields.Char(
        string='Product Barcode (EAN13)',
        help="This field is designed to be filled with a barcode reader")
    product_id = fields.Many2one(
        'product.product', string='Product', required=True)

    @api.onchange('product_barcode')
    def product_barcode_change(self):
        if self.product_barcode:
            products = self.env['product.product'].search([
                ('ean13', '=', self.product_barcode)])
            if len(products) == 1:
                self.product_id = products[0]
                self.create_sale_order_line()
                self.product_barcode = ""
                self.product_id = False
            elif len(products) > 1:
                return {'warning': {
                    'title': _('Error'),
                    'message': _(
                        'Several products have been found '
                        'with this code as EAN13 or Internal Reference:\n %s'
                        '\nYou should select the right product manually.'
                        ) % '\n'.join([
                            product.name_get()[0][1] for product in products
                        ])}}
            else:
                return {'warning': {
                    'title': _('Error'),
                    'message': _(
                        'No product found with this code as '
                        'EAN13 nor Internal Reference. You should select '
                        'the right product manually.')}}

    def create_sale_order_line(self):
        obj_sale_order_line = self.env['sale.order.line']
        active_id = self._context['active_id']

        lines = obj_sale_order_line.search([
            ('order_id', '=', active_id),
            ('product_id', '=', self.product_id.id),
        ])

        if lines:
            lines.write({'product_uom_qty': lines.product_uom_qty + 1})
        else:
            obj_sale_order_line.create({
                'order_id': active_id,
                'product_id': self.product_id.id,
            })

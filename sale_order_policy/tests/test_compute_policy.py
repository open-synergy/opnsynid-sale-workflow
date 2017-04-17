# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestComputeOrderPolicy(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestComputeOrderPolicy, self).setUp(*args, **kwargs)
        # Objects
        self.obj_sale_order = self.env['sale.order']
        self.obj_res_groups = self.env['res.groups']
        self.obj_res_users = self.env['res.users']

        # Data
        self.partner = self.env.ref('base.res_partner_3')
        self.product =\
            self.env.ref('product.product_product_13')
        self.so_type_normal =\
            self.env.ref("sale_order_type.normal_sale_type")
        self.group_employee_id = self.ref('base.group_user')
        self.grp_so_manager =\
            self.env.ref(
                'base.group_sale_manager')
        self.user_1 = self._create_user_1()
        self.user_2 = self._create_user_2()
        self.user_3 = self._create_user_3()

        # Add Group Recreate Invoice
        self.grp_invoice_recreate = self.obj_res_groups.create({
            'name': 'Normal - Group Button Recreate Invoice'
        })
        # Add Group Button Ignore Exception
        self.grp_invoice_corrected = self.obj_res_groups.create({
            'name': 'Normal - Group Button Ignore Exception'
        })
        # Add Group Button Send by Email
        self.grp_quotation_send = self.obj_res_groups.create({
            'name': 'Normal - Group Button Send by Email'
        })
        # Add Group Button Confirm Order
        self.grp_confirm_order = self.obj_res_groups.create({
            'name': 'Normal - Group Button Confirm Order'
        })
        # Add Group Button View Invoice
        self.grp_view_invoice = self.obj_res_groups.create({
            'name': 'Normal - Group Button View Invoice'
        })
        # Add Group Button Create Invoice
        self.grp_create_invoice = self.obj_res_groups.create({
            'name': 'Normal - Group Button Create Invoice'
        })
        # Add Group Button New Copy of Quotation
        self.grp_copy_quotation = self.obj_res_groups.create({
            'name': 'Normal - Group Button New Copy of Quotation'
        })
        # Add Group Button Cancel Quotation
        self.grp_cancel_quot = self.obj_res_groups.create({
            'name': 'Normal - Group Button Cancel Quotation'
        })
        # Add Group Button Cancel Order
        self.grp_cancel_order = self.obj_res_groups.create({
            'name': 'Normal - Group Button Cancel Order'
        })

    def _create_user_1(self):
        val = {
            'name': 'User Test 1',
            'login': 'user_1',
            'alias_name': 'user1',
            'email': 'user_test_1@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_so_manager.id
                ]
            )]
        }
        user_1 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_1

    def _create_user_2(self):
        val = {
            'name': 'User Test 2',
            'login': 'user_2',
            'alias_name': 'user2',
            'email': 'user_test_2@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_so_manager.id
                ]
            )]
        }
        user_2 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_2

    def _create_user_3(self):
        val = {
            'name': 'User Test 3',
            'login': 'user_3',
            'alias_name': 'user3',
            'email': 'user_test_3@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_so_manager.id
                ]
            )]
        }
        user_3 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_3

    def _create_sale_order(self, order_type_id):
        if order_type_id:
            type_id = order_type_id.id
        else:
            type_id = False

        sale_order_dict = {}
        sale_line_dict = {}
        # Create Sale Order
        sale_order_dict['partner_id'] = self.partner.id
        sale_order_dict['type_id'] = type_id
        sale_line_dict = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 1.0,
            'price_unit': self.product.lst_price,
        }
        sale_order_dict['order_line'] = [(0, 0, sale_line_dict)]
        sale_order = self.obj_sale_order.create(sale_order_dict)

        return sale_order

    def test_compute_case_admin(self):
        # Create Sale Order
        sale_order =\
            self._create_sale_order(False)

        # Condition :
        #   1. Test for User Admin
        self.assertEqual(True, sale_order.invoice_recreate_ok)
        self.assertEqual(True, sale_order.invoice_corrected_ok)
        self.assertEqual(True, sale_order.quotation_send_ok)
        self.assertEqual(True, sale_order.confirm_order_ok)
        self.assertEqual(True, sale_order.view_invoice_ok)
        self.assertEqual(True, sale_order.create_invoice_ok)
        self.assertEqual(True, sale_order.copy_quotation_ok)
        self.assertEqual(True, sale_order.cancel_quot_ok)
        self.assertEqual(True, sale_order.cancel_order_ok)

    def test_compute_case_no_type(self):
        # Create Sale Order
        sale_order =\
            self._create_sale_order(False)

        # Condition :
        #   1. No Sale Order Type
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).invoice_recreate_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).invoice_corrected_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).quotation_send_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).view_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).create_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).copy_quotation_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).cancel_quot_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).cancel_order_ok
        )

    def test_compute_case_1(self):
        # Create Sale Order
        sale_order =\
            self._create_sale_order(self.so_type_normal)

        # Condition :
        #   1. Log In As User 1
        #   2. Allowed to Recreate Invoice has group
        #   3. Allowed to Ignore Exception has group
        #   4. Allowed to Send by Email has group
        #   6. User 1 doesn't have group
        self.so_type_normal.invoice_recreate_group_ids = [(
            6, 0, [
                self.grp_invoice_recreate.id
            ]
        )]

        self.so_type_normal.invoice_corrected_group_ids = [(
            6, 0, [
                self.grp_invoice_corrected.id
            ]
        )]

        self.so_type_normal.quotation_send_group_ids = [(
            6, 0, [
                self.grp_quotation_send.id
            ]
        )]

        # Result
        #   1. User 1 cannot Recreate Invoice
        #   2. User 1 cannot Ignore Exception
        #   3. User 1 cannot Send by Email

        self.assertEqual(
            False,
            sale_order.sudo(
                self.user_1.id).invoice_recreate_ok
        )
        self.assertEqual(
            False,
            sale_order.sudo(
                self.user_1.id).invoice_corrected_ok
        )
        self.assertEqual(
            False,
            sale_order.sudo(
                self.user_1.id).quotation_send_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).view_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).create_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).copy_quotation_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).cancel_quot_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).cancel_order_ok
        )

        # Condition :
        #   1. User 1 have group
        # Add Group Recreate Invoice
        self.user_1.groups_id = [(
            4,
            self.grp_invoice_recreate.id
        )]
        # Add Group Ignore Exception
        self.user_1.groups_id = [(
            4,
            self.grp_invoice_corrected.id
        )]
        # Add Group Send by Email
        self.user_1.groups_id = [(
            4,
            self.grp_quotation_send.id
        )]

        # Result
        #   1. User 1 can Recreate Invoice
        #   2. User 1 can Ignore Exception
        #   3. User 1 can Send by Email
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).invoice_recreate_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).invoice_corrected_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).quotation_send_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).view_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).create_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).copy_quotation_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).cancel_quot_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_1.id).cancel_order_ok
        )

    def test_compute_case_2(self):
        # Create Sale Order
        sale_order =\
            self._create_sale_order(self.so_type_normal)

        # Condition :
        #   1. Log In As User 2
        #   2. Allowed to Confirm Sale has group
        #   3. Allowed to View Invoice has group
        #   4. Allowed to Create Invoice has group
        #   6. User 2 doesn't have group
        self.so_type_normal.confirm_order_group_ids = [(
            6, 0, [
                self.grp_confirm_order.id
            ]
        )]

        self.so_type_normal.view_invoice_group_ids = [(
            6, 0, [
                self.grp_view_invoice.id
            ]
        )]

        self.so_type_normal.create_invoice_group_ids = [(
            6, 0, [
                self.grp_create_invoice.id
            ]
        )]

        # Result
        #   1. User 2 cannot Confirm Sale
        #   2. User 2 cannot View Invoice
        #   3. User 2 cannot Create Invoice

        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).invoice_recreate_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).invoice_corrected_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).quotation_send_ok
        )
        self.assertEqual(
            False,
            sale_order.sudo(
                self.user_2.id).confirm_order_ok
        )
        self.assertEqual(
            False,
            sale_order.sudo(
                self.user_2.id).view_invoice_ok
        )
        self.assertEqual(
            False,
            sale_order.sudo(
                self.user_2.id).create_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).copy_quotation_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).cancel_quot_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).cancel_order_ok
        )

        # Condition :
        #   1. User 2 have group
        # Add Group Confirm Sale
        self.user_2.groups_id = [(
            4,
            self.grp_confirm_order.id
        )]
        # Add Group View Invoice
        self.user_2.groups_id = [(
            4,
            self.grp_view_invoice.id
        )]
        # Add Group Create Invoice
        self.user_2.groups_id = [(
            4,
            self.grp_create_invoice.id
        )]

        # Result
        #   1. User 2 can Confirm Sale
        #   2. User 2 can View Invoice
        #   3. User 2 can Create Invoice
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).invoice_recreate_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).invoice_corrected_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).quotation_send_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).view_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).create_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).copy_quotation_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).cancel_quot_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_2.id).cancel_order_ok
        )

    def test_compute_case_3(self):
        # Create Sale Order
        sale_order =\
            self._create_sale_order(self.so_type_normal)

        # Condition :
        #   1. Log In As User 3
        #   2. Allowed to New Copy of Quotation has group
        #   3. Allowed to Cancel Quotation has group
        #   4. Allowed to Cancel Order has group
        #   6. User 3 doesn't have group
        self.so_type_normal.copy_quotation_group_ids = [(
            6, 0, [
                self.grp_copy_quotation.id
            ]
        )]

        self.so_type_normal.cancel_quot_group_ids = [(
            6, 0, [
                self.grp_cancel_quot.id
            ]
        )]

        self.so_type_normal.cancel_order_group_ids = [(
            6, 0, [
                self.grp_cancel_order.id
            ]
        )]

        # Result
        #   1. User 3 cannot New Copy of Quotation
        #   2. User 3 cannot Cancel Quotation
        #   3. User 3 cannot Cancel Order

        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).invoice_recreate_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).invoice_corrected_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).quotation_send_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).view_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).create_invoice_ok
        )
        self.assertEqual(
            False,
            sale_order.sudo(
                self.user_3.id).copy_quotation_ok
        )
        self.assertEqual(
            False,
            sale_order.sudo(
                self.user_3.id).cancel_quot_ok
        )
        self.assertEqual(
            False,
            sale_order.sudo(
                self.user_3.id).cancel_order_ok
        )

        # Condition :
        #   1. User 3 have group
        # Add Group New Copy of Quotation
        self.user_3.groups_id = [(
            4,
            self.grp_copy_quotation.id
        )]
        # Add Group Cancel Quotation
        self.user_3.groups_id = [(
            4,
            self.grp_cancel_quot.id
        )]
        # Add Group Cancel Order
        self.user_3.groups_id = [(
            4,
            self.grp_cancel_order.id
        )]

        # Result
        #   1. User 3 can New Copy of Quotation
        #   2. User 3 can Cancel Quotation
        #   3. User 3 can Cancel Order
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).invoice_recreate_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).invoice_corrected_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).quotation_send_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).view_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).create_invoice_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).copy_quotation_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).cancel_quot_ok
        )
        self.assertEqual(
            True,
            sale_order.sudo(
                self.user_3.id).cancel_order_ok
        )

# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Datetime
from odoo.tests.common import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestStockPicking(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.res_partner_4")
        cls.product = cls.env.ref("product.product_product_13")
        cls.product_uom = cls.env.ref("uom.product_uom_unit")
        cls.picking_type_debit = cls.env["stock.picking.type"].create(
            {
                "name": "Debit Operation",
                "sequence_code": "DebitOperation",
                "code": "outgoing",
                "compute_analytic_value": "debit",
            }
        )
        cls.picking_type_credit = cls.env["stock.picking.type"].create(
            {
                "name": "Credit Operation",
                "sequence_code": "CreditOperation",
                "code": "outgoing",
                "compute_analytic_value": "credit",
            }
        )
        cls.location = cls.env.ref("stock.stock_location_suppliers")
        cls.location_dest = cls.env.ref("stock.stock_location_customers")
        cls.analytic_account = cls.env.ref("analytic.analytic_agrolait")
        cls.picking_debit = cls.env["stock.picking"].create(
            {
                "partner_id": cls.partner.id,
                "scheduled_date": Datetime.now(),
                "picking_type_id": cls.picking_type_debit.id,
                "location_id": cls.location.id,
                "location_dest_id": cls.location_dest.id,
                "move_line_ids_without_package": [
                    (
                        0,
                        0,
                        {
                            "qty_done": 5.0,
                            "product_id": cls.product.id,
                            "product_uom_id": cls.product_uom.id,
                            "location_id": cls.location.id,
                            "location_dest_id": cls.location_dest.id,
                            "analytic_account_id": cls.analytic_account.id,
                        },
                    )
                ],
            }
        )
        cls.picking_credit = cls.env["stock.picking"].create(
            {
                "partner_id": cls.partner.id,
                "scheduled_date": Datetime.now(),
                "picking_type_id": cls.picking_type_credit.id,
                "location_id": cls.location.id,
                "location_dest_id": cls.location_dest.id,
                "move_line_ids_without_package": [
                    (
                        0,
                        0,
                        {
                            "qty_done": 5.0,
                            "product_id": cls.product.id,
                            "product_uom_id": cls.product_uom.id,
                            "location_id": cls.location.id,
                            "location_dest_id": cls.location_dest.id,
                            "analytic_account_id": cls.analytic_account.id,
                        },
                    )
                ],
            }
        )

    def test_create_analytic_entry_debit(self):
        # Execute the _create_analytic_entry method
        self.picking_debit._create_analytic_entry()

        # Check if analytic lines were created
        analytic_lines = self.env["account.analytic.line"].search(
            [("picking_origin", "=", self.picking_debit.id)]
        )
        self.assertTrue(analytic_lines, "Analytic lines were not created")

        # Check the unit_amount values for the analytic lines
        for line in analytic_lines:
            self.assertEqual(line.unit_amount, 5.0)
            self.assertEqual(line.name, self.picking_debit.name)
            self.assertEqual(line.product_id, self.product)
            # Check amount return type debit (negative)
            self.assertTrue(line.amount < 0)

    def test_create_analytic_entry_credit(self):
        # Execute the _create_analytic_entry method
        self.picking_credit._create_analytic_entry()

        # Check if analytic lines were created
        analytic_lines = self.env["account.analytic.line"].search(
            [("picking_origin", "=", self.picking_credit.id)]
        )
        self.assertTrue(analytic_lines, "Analytic lines were not created")

        # Check the unit_amount values for the analytic lines
        for line in analytic_lines:
            self.assertEqual(line.unit_amount, 5.0)
            self.assertEqual(line.name, self.picking_credit.name)
            self.assertEqual(line.product_id, self.product)
            # Check amount return type credit (positive)
            self.assertTrue(line.amount > 0)

        # Call action analytic line tree
        action = self.picking_credit.action_analytic_line_tree()

        # Check action is disct
        self.assertIsInstance(action, dict, "The action should be a dictionary")

        # Check dict action
        self.assertEqual(
            action.get("name"),
            "Analytic Line Operations",
            "The action name is incorrect",
        )
        self.assertEqual(
            action.get("type"), "ir.actions.act_window", "The action type is incorrect"
        )
        self.assertEqual(
            action.get("res_model"),
            "account.analytic.line",
            "The res_model is incorrect",
        )

        # Check domain in action
        domain = action.get("domain")
        self.assertIsInstance(domain, list, "The domain should be a list")
        self.assertIn(
            ("picking_origin", "=", self.picking_credit.id),
            domain,
            "The domain is incorrect",
        )

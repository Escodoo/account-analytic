# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    has_analytic_line = fields.Boolean(compute="_compute_has_analytic_line")

    def _create_analytic_entry(self):
        for picking in self:
            lines = picking.move_line_ids_without_package.filtered(
                lambda line: line.analytic_account_id and line.qty_done > 0
            )
            for line in lines:
                amount = line.product_id.standard_price * line.qty_done
                if self.picking_type_id.compute_analytic_value == "credit":
                    self.env["account.analytic.line"].create(
                        {
                            "name": picking.name,
                            "account_id": line.analytic_account_id.id,
                            "amount": amount,
                            "unit_amount": line.qty_done,
                            "product_id": line.product_id.id,
                            "product_uom_id": line.product_id.uom_id.id,
                            "picking_origin": picking.id,
                        }
                    )
                elif self.picking_type_id.compute_analytic_value == "debit":
                    self.env["account.analytic.line"].create(
                        {
                            "name": picking.name,
                            "account_id": line.analytic_account_id.id,
                            "amount": -amount,
                            "unit_amount": line.qty_done,
                            "product_id": line.product_id.id,
                            "product_uom_id": line.product_id.uom_id.id,
                            "picking_origin": picking.id,
                        }
                    )

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self._create_analytic_entry()
        return res

    def _compute_has_analytic_line(self):
        for picking in self:
            picking.has_analytic_line = bool(
                self.env["account.analytic.line"].search_count(
                    [("picking_origin", "=", picking.id)]
                )
            )

    def action_analytic_line_tree(self):
        return {
            "name": "Analytic Line Operations",
            "type": "ir.actions.act_window",
            "res_model": "account.analytic.line",
            "view_mode": "tree",
            "view_id": self.env.ref("analytic.view_account_analytic_line_tree").id,
            "domain": [("picking_origin", "=", self.id)],
        }

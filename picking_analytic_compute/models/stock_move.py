# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    picking_line_cost = fields.Float(
        compute="_compute_picking_subtotal",
        string="Subtotal",
        readonly=True,
    )

    @api.depends("product_id", "quantity_done")
    def _compute_picking_subtotal(self):
        for line in self:
            line.picking_line_cost = line.quantity_done * line.product_id.standard_price


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    picking_line_cost = fields.Float(
        compute="_compute_picking_subtotal",
        string="Subtotal",
        readonly=True,
    )

    @api.depends("product_id", "qty_done")
    def _compute_picking_subtotal(self):
        for line in self:
            line.picking_line_cost = line.qty_done * line.product_id.standard_price

# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPickingType(models.Model):

    _inherit = "stock.picking.type"

    compute_analytic_value = fields.Selection(
        [
            ("debit", "Debit"),  # Operation type debit
            ("credit", "Credit"),  # Operation type credit
        ],
    )

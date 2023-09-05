# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    picking_origin = fields.Many2one(
        "stock.picking",
    )

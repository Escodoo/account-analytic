# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Picking Analytic Compute",
    "summary": """
        Picking Analytic Compute""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-analytic",
    "depends": ["stock_analytic"],
    "data": [
        "views/stock_move_line_views.xml",
        "views/stock_picking_views.xml",
        "views/account_analytic.view.xml",
    ],
}

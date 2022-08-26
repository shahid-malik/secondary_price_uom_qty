# Copyright 2018-2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Secondary Unit",
    "summary": "Sale product in a secondary unit",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Sale",
    "website": "https://www.mediodconsulting.com/",
    "author": "Shahid Mehmood",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": ["sale", "product_secondary_unit"],
    "data": [
        "views/product_views.xml",
        "views/sale_order_views.xml",
        "views/invoice_views.xml",
        "views/stock_view_picking.xml",
        "views/invoice_report_inherit.xml",
        "report/sale_report_templates.xml",
    ],
}

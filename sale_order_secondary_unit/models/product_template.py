# Copyright 2018-2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_default_sale_price(self):
        print(self)
        self.secondary_sale_price = self.list_price

    sale_secondary_uom_id = fields.Many2one(
        comodel_name="uom.uom", string="Secondary unit for Sales"
    )
    secondary_sale_price = fields.Float('2nd Sale Price', compute=_get_default_sale_price)

    @api.onchange('uom_po_id')
    def onchange_uom_po_id(self):
        categ_id = self.uom_id.category_id
        return {
            'domain': {'purchase_secondary_uom_id': [('category_id', '=', categ_id.id)]}
        }


class ProductCategory(models.Model):
    _inherit = 'product.category'

    secondary_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="2nd UoM",
    )
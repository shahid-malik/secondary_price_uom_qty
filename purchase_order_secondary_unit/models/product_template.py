# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"


    purchase_secondary_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="2nd unit for Purchases",
    )

    secondary_purchase_price = fields.Float('Secondary Purchase Price')


    @api.onchange('uom_id')
    def onchange_uom(self):
        categ_id =  self.uom_id.category_id
        return{
            'domain': {'sale_secondary_uom_id': [('category_id', '=', categ_id.id)]}
        }
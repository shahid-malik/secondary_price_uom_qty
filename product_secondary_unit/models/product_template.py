# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    secondary_uom_ids = fields.One2many(
        comodel_name="product.secondary.unit",
        inverse_name="product_tmpl_id",
        string="Secondary Unit of Measure",
        help="Default Secondary Unit of Measure.",
        context={"active_test": False},
    )

    editable_subtotal = fields.Boolean(string="Editable Subtotal",default=False)
    editable_uom = fields.Boolean(default=False, string="Editable UoM")
    editable_second_quantity = fields.Boolean(default=False, string="Editable 2nd Quantity")
    editable_second_uom = fields.Boolean(default=True, string="Editable 2nd UoM")

    disable_subtotal = fields.Boolean(default=False, string="Disable Subtotal")
    disable_uom = fields.Boolean(default=True, string="Disable UoM")
    disable_second_quantity = fields.Boolean(default=True, string="Disable 2nd Quantity")
    disable_second_uom = fields.Boolean(default=True, string="Disable 2nd UoM")



    @api.onchange("disable_second_uom", "disable_second_quantity")
    def onchange_disable_second_uom(self):
        if self.disable_second_uom == True:
            self.secondary_sale_price = 0
            self.secondary_purchase_price = 0
        elif self.disable_second_uom == False:
            self.secondary_sale_price = self.list_price
            self.secondary_purchase_price = self.list_price



    @api.model
    def _get_default_secondary_uom(self):
        return (
            self.secondary_uom_ids
            and self.secondary_uom_ids[0]
            or self.secondary_uom_ids
        )

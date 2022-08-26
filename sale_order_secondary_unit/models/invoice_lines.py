from odoo import fields, models, api


class InvoiceLines(models.Model):
    _inherit = "account.move.line"

    secondary_uom_qty = fields.Float(
            string="2nd Qty", digits="Product Unit of Measure", default=1.0
        )
    # secondary_uom_id = fields.Many2one(
    #     comodel_name="product.secondary.unit",
    #     string="2nd UoM",
    #     ondelete="restrict",
    # )
    secondary_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="2nd UoM",
        ondelete="restrict",
    )
    secondary_price = fields.Float('2nd Price', default=1.0)

    @api.onchange("product_id")
    def product_id_change(self):
        print(self)
        if self.product_id.secondary_sale_price > 0.0:
            self.secondary_price = self.product_id.secondary_sale_price
        self.secondary_uom_id = self.product_id.sale_secondary_uom_id

    # @api.onchange("product_uom_id")
    # def product_uom_id_invoice(self):
    #     categ_id = self.product_uom_id
    #     self.secondary_uom_id = categ_id.id

# Copyright 2018-2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.float_utils import float_compare, float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    secondary_uom_qty = fields.Float(
        string="2nd Qty", digits="Product Unit of Measure", default=1.0
    )
    secondary_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="2nd UoM",
        ondelete="restrict",
    )
    secondary_sale_price = fields.Float('2nd Price', default=0.0)

    @api.onchange("secondary_uom_id", "secondary_uom_qty")
    def onchange_secondary_uom(self):
        if not self.secondary_uom_id:
            return
        # factor = self.secondary_uom_id.factor * self.product_uom.factor
        factor = self.secondary_uom_id.factor_inv
        qty = float_round(
            self.secondary_uom_qty * factor,
            precision_rounding=self.product_uom.rounding,
        )
        if (
                float_compare(
                    self.product_uom_qty, qty, precision_rounding=self.product_uom.rounding
                )
                != 0
        ):
            self.product_uom_qty = qty
            self.secondary_sale_price = self.price_unit * factor

    @api.onchange("product_uom_qty")
    def onchange_secondary_unit_product_uom_qty(self):
        if not self.secondary_uom_id:
            return
        # factor = self.secondary_uom_id.factor * self.product_uom.factor
        factor = self.secondary_uom_id.factor_inv
        # qty = float_round(
        #     self.product_uom_qty / (factor or 1.0),
        #     precision_rounding=self.secondary_uom_id.uom_id.rounding,
        # )
        qty = float_round(
            # self.product_uom_qty / (factor or 1.0),
            self.product_uom_qty / (factor or 1.0),
            precision_rounding=self.secondary_uom_id.rounding,
        )
        if (
                # float_compare(
                #     self.secondary_uom_qty,
                #     qty,
                #     precision_rounding=self.secondary_uom_id.uom_id.rounding,
                # )
                float_compare(
                    self.secondary_uom_qty,
                    qty,
                    precision_rounding=self.secondary_uom_id.rounding,
                )
                != 0
        ):
            self.secondary_uom_qty = qty
            self.secondary_sale_price = self.price_unit * factor

    @api.onchange("product_uom")
    def onchange_product_uom_for_secondary(self):
        if not self.secondary_uom_id:
            return
        factor = self.product_uom.factor * self.secondary_uom_id.factor
        qty = float_round(
            self.product_uom_qty / (factor or 1.0),
            precision_rounding=self.product_uom.rounding,
        )
        if (
                float_compare(
                    self.secondary_uom_qty,
                    qty,
                    precision_rounding=self.product_uom.rounding,
                )
                != 0
        ):
            self.secondary_uom_qty = qty

    @api.onchange("product_id")
    def product_id_change(self):
        """
        If default sales secondary unit set on product, put on secondary
        quantity 1 for being the default quantity. We override this method,
        that is the one that sets by default 1 on the other quantity with that
        purpose.
        """
        res = super().product_id_change()
        self.secondary_uom_qty = 1.0
        if self.price_unit >= 0:
            self.secondary_sale_price = self.price_unit
        elif self.price_unit == 0:
            self.secondary_sale_price = 0
        self.secondary_uom_id = self.product_id.sale_secondary_uom_id
        if self.secondary_uom_id:
            self.secondary_uom_qty = 1.0
            self.secondary_sale_price = self.price_unit
            # self.secondary_purchase_price = self.price_unit
            self.onchange_secondary_uom()

        if self.product_uom.name == 'CTN of 10' and self.secondary_uom_id == 'CTN of Mix Kg':
            self.secondary_sale_price = self.price_unit / self.secondary_sale_price

        elif self.product_uom.name == 'CTN of Mix Kg' and self.secondary_uom_id == 'CTN of 10':
            self.secondary_sale_price = self.price_unit * self.secondary_sale_price

        # calc 2nd price
        if self.secondary_uom_id and self.price_unit:
            self.secondary_sale_price = self.secondary_uom_id.factor * self.price_unit
        return res

    @api.onchange('price_subtotal')
    def onchange_price_subtotal(self):
        if self.price_subtotal and self.price_unit:
            self.product_uom_qty = self.price_subtotal / self.price_unit

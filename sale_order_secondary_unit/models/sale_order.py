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

    @api.onchange("product_uom")
    def _onchange_product_uom(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_uom_qty or 1.0
                self.secondary_sale_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.secondary_uom_qty = (self.product_uom_qty * uom_factor) / sec_uom_factor
                self.secondary_sale_price = (self.price_unit / uom_factor) * sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.secondary_uom_qty = (self.product_uom_qty / sec_uom_factor) * uom_factor
                self.secondary_sale_price = (self.price_unit * sec_uom_factor) / uom_factor or 0.0

    @api.onchange("secondary_uom_id")
    def _onchange_second_uom_id(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_uom_qty or 1.0
                self.secondary_sale_price = self.price_unit or 0.0
            elif uom_factor > sec_uom_factor:
                self.secondary_uom_qty = (self.product_uom_qty * uom_factor) / sec_uom_factor
                self.secondary_sale_price = (self.price_unit / uom_factor) * sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.secondary_uom_qty = (self.product_uom_qty / sec_uom_factor) * uom_factor
                self.secondary_sale_price = (self.price_unit * sec_uom_factor) / uom_factor or 0.0

    @api.onchange("price_unit")
    def _onchange_unit_price(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_uom_qty or 1.0
                self.secondary_sale_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.secondary_sale_price = (self.price_unit / uom_factor) * sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.secondary_sale_price = (self.price_unit *  sec_uom_factor) / uom_factor

    @api.onchange("product_uom_qty")
    def _onchange_product_qty(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_uom_qty or 1.0
                self.secondary_sale_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.secondary_uom_qty = (self.product_uom_qty * uom_factor) / sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.secondary_uom_qty = (self.product_uom_qty / sec_uom_factor) * uom_factor

    @api.onchange("secondary_uom_qty")
    def _onchange_second_qty(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_uom_qty or 1.0
                self.secondary_sale_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.product_uom_qty = (self.secondary_uom_qty / uom_factor) * sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.product_uom_qty = (self.secondary_uom_qty * sec_uom_factor) / uom_factor

    @api.onchange("secondary_sale_price")
    def _onchange_secondary_price(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_uom_qty or 1.0
                self.secondary_sale_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.price_unit = (self.secondary_sale_price * uom_factor) / sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.price_unit = (self.secondary_sale_price / sec_uom_factor) * uom_factor

    @api.onchange("price_subtotal")
    def _onchange_subtotal_amount(self):
        if self.price_subtotal and self.product_uom_qty > 0:
            self.price_unit = self.price_subtotal / self.product_uom_qty

    # @api.onchange("secondary_uom_id")
    # def onchange_secondary_uom(self):
    #     if not self.secondary_uom_id:
    #         return
    #     if self.product_id.is_secondary_conversions:
    #         factor = self.secondary_uom_id.factor_inv
    #         qty = float_round(
    #             self.product_uom_qty / factor,
    #             precision_rounding=self.product_uom.rounding,
    #         )
    #         if (
    #                 float_compare(
    #                     self.product_uom_qty, qty, precision_rounding=self.product_uom.rounding
    #                 )
    #                 != 0
    #         ):
    #             self.secondary_uom_qty = qty
    #             self.secondary_sale_price = self.price_unit * factor
    #     else:
    #         self.secondary_sale_price = self.price_unit
    #         self.secondary_uom_qty = self.secondary_uom_id.factor_inv if self.secondary_uom_id else False
    #
    # @api.onchange("secondary_uom_qty")
    # def _onchange_secondary_qty(self):
    #     if not self.secondary_uom_id:
    #         return
    #     if self.product_id.is_secondary_conversions:
    #         factor = self.secondary_uom_id.factor_inv
    #         if factor > self.product_uom.factor_inv:
    #             qty = float_round(
    #                 self.secondary_uom_qty * factor,
    #                 precision_rounding=self.product_uom.rounding,
    #             )
    #             if (
    #                     float_compare(
    #                         self.product_uom_qty, qty, precision_rounding=self.product_uom.rounding
    #                     )
    #                     != 0
    #             ):
    #                 self.product_uom_qty = qty
    #
    # @api.onchange("product_uom_qty")
    # def onchange_secondary_unit_product_uom_qty(self):
    #     if not self.secondary_uom_id:
    #         return
    #
    #     if not self.product_id.is_secondary_conversions:
    #         self.secondary_sale_price = self.price_unit
    #         self.secondary_uom_qty = self.secondary_uom_id.factor_inv
    #         return
    #
    #     if self.product_id.is_secondary_conversions:
    #         factor = self.secondary_uom_id.factor_inv
    #         if self.secondary_uom_id.factor_inv > self.product_uom.factor_inv:
    #             factor = self.secondary_uom_id.factor_inv or 1.0
    #             qty = float_round(
    #                 self.product_uom_qty / factor,
    #                 precision_rounding=self.secondary_uom_id.rounding,
    #             )
    #             if (
    #                     float_compare(
    #                         self.secondary_uom_qty,
    #                         qty,
    #                         precision_rounding=self.secondary_uom_id.rounding,
    #                     )
    #                     != 0
    #             ):
    #                 self.secondary_uom_qty = qty
    #                 self.secondary_sale_price = self.price_unit * factor
    #         elif  self.secondary_uom_id.factor_inv < self.product_uom.factor_inv:
    #             factor = self.product_uom.factor_inv or 1.0
    #             qty = float_round(
    #                 self.product_uom_qty * (factor or 1.0),
    #                 precision_rounding=self.secondary_uom_id.rounding,
    #             )
    #             if (
    #                     float_compare(
    #                         self.secondary_uom_qty,
    #                         qty,
    #                         precision_rounding=self.secondary_uom_id.rounding,
    #                     )
    #                     != 0
    #             ):
    #                 self.secondary_uom_qty = qty
    #                 self.secondary_sale_price = self.price_unit / factor
    #
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

        if self.product_uom.name == 'CTN of 10' and self.secondary_uom_id == 'CTN of Mix Kg':
            self.secondary_sale_price = self.price_unit / self.secondary_sale_price

        elif self.product_uom.name == 'CTN of Mix Kg' and self.secondary_uom_id == 'CTN of 10':
            self.secondary_sale_price = self.price_unit * self.secondary_sale_price

        # calc 2nd price
        # if self.secondary_uom_id and self.price_unit:
        #     self.secondary_sale_price = self.secondary_uom_id.factor_inv * self.price_unit
        return res
    #
    # @api.onchange("price_subtotal")
    # def onchange_price_subtotal(self):
    #     if self.price_subtotal and self.price_unit:
    #         self.product_uom_qty = self.price_subtotal / self.price_unit
    #
    # @api.onchange("price_unit")
    # def _onchange_price_unit(self):
    #     if self.product_id.is_secondary_conversions:
    #         if self.secondary_uom_id.factor_inv > self.product_uom.factor_inv:
    #             self.secondary_sale_price = self.price_unit * self.secondary_uom_id.factor_inv
    #         else:
    #             self.secondary_sale_price = self.price_unit / self.product_uom.factor_inv
    #     else:
    #         self.secondary_sale_price = self.price_unit
    #
    # @api.onchange("secondary_sale_price")
    # def onchange_secondary_sale_price(self):
    #     if self.product_id.is_secondary_conversions:
    #         factor = self.secondary_uom_id.factor_inv
    #         if factor > self.product_uom.factor_inv:
    #             self.price_unit = self.secondary_sale_price / factor
    #
    # @api.onchange("product_uom")
    # def _onchange_product_uom(self):
    #     if self.product_uom.uom_type != 'reference':
    #         factor = self.product_uom.factor_inv or 1.0
    #         sec_factor = self.secondary_uom_id.factor_inv or 1.0
    #         if self.product_uom.uom_type == "bigger":
    #             self.secondary_uom_qty = self.product_uom_qty * factor
    #             self.secondary_sale_price = (self.price_unit / factor)/sec_factor




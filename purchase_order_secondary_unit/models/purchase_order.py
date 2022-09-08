# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.float_utils import float_compare, float_round


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    secondary_uom_qty = fields.Float(
        string="2nd QTY", digits="Product Unit of Measure", default=1.0
    )
    secondary_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="2nd UOM",
        ondelete="restrict",
    )
    secondary_purchase_price = fields.Float('2nd Purchase Price', default=0.0)

    @api.onchange('product_id')
    def _onchange_po_product_id(self):
        # self.product_qty = 1.0
        if self.product_id.is_secondary_conversions:
            self.secondary_uom_id = self.product_id.purchase_secondary_uom_id
            factor = self.product_id.purchase_secondary_uom_id.factor_inv or 1.0
            self.secondary_uom_qty = self.product_qty / factor
            self.secondary_purchase_price = self.secondary_uom_qty * self.price_unit
        else:
            self.secondary_uom_id = self.product_id.purchase_secondary_uom_id or False
            self.secondary_uom_qty = self.product_id.purchase_secondary_uom_id.factor_inv or 1.0
            self.secondary_purchase_price = self.price_unit

    @api.onchange("product_uom")
    def _onchange_product_uom(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_qty or 1.0
                self.secondary_purchase_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.secondary_uom_qty = (self.product_qty * uom_factor) / sec_uom_factor
                self.secondary_purchase_price = (self.price_unit / uom_factor) * sec_uom_factor or 0.0
            elif uom_factor < sec_uom_factor:
                self.secondary_uom_qty = (self.product_qty / sec_uom_factor) * uom_factor
                self.secondary_purchase_price = (self.price_unit * sec_uom_factor) / uom_factor or 0.0

    @api.onchange("secondary_uom_id")
    def _onchange_second_uom_id(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_qty or 1.0
                self.secondary_purchase_price = self.price_unit or 0.0
            elif uom_factor > sec_uom_factor:
                self.secondary_uom_qty = (self.product_qty * uom_factor) / sec_uom_factor
                self.secondary_purchase_price = (self.price_unit / uom_factor) * sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.secondary_uom_qty = (self.product_qty / sec_uom_factor) * uom_factor
                self.secondary_purchase_price = (self.price_unit * sec_uom_factor) / uom_factor or 0.0

    @api.onchange("price_unit")
    def _onchange_unit_price(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_qty or 1.0
                self.secondary_sale_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.secondary_purchase_price = (self.price_unit / uom_factor) * sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.secondary_purchase_price = (self.price_unit * sec_uom_factor) / uom_factor

    @api.onchange("product_qty")
    def _onchange_product_qty(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_qty or 1.0
                self.secondary_purchase_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.secondary_uom_qty = (self.product_qty * uom_factor) / sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.secondary_uom_qty = (self.product_qty / sec_uom_factor) * uom_factor

    @api.onchange("secondary_uom_qty")
    def _onchange_second_qty(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_qty or 1.0
                self.secondary_purchase_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.product_qty = (self.secondary_uom_qty / uom_factor) * sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.product_qty = (self.secondary_uom_qty * sec_uom_factor) / uom_factor

    @api.onchange("secondary_purchase_price")
    def _onchange_secondary_price(self):
        if self.product_id.is_secondary_conversions:
            uom_factor = self.product_uom.factor_inv or 1.0
            sec_uom_factor = self.secondary_uom_id.factor_inv or 1.0
            if self.product_uom == self.secondary_uom_id:
                self.secondary_uom_qty = self.product_uom_qty or 1.0
                self.secondary_purchase_price = self.price_unit
            elif uom_factor > sec_uom_factor:
                self.price_unit = (self.secondary_purchase_price * uom_factor) / sec_uom_factor
            elif uom_factor < sec_uom_factor:
                self.price_unit = (self.secondary_purchase_price / sec_uom_factor) * uom_factor

    @api.onchange("price_subtotal")
    def _onchange_subtotal_amount(self):
        if self.price_subtotal and self.product_qty > 0:
            self.price_unit = self.price_subtotal / self.product_qty

    # @api.onchange("secondary_uom_id")
    # def _onchange_secondary_uom(self):
    #     if not self.secondary_uom_id:
    #         return
    #     # factor = self.secondary_uom_id.factor * self.product_uom.factor
    #     factor = self.secondary_uom_id.factor_inv
    #     qty = float_round(
    #         self.product_qty / factor,
    #         precision_rounding=self.product_uom.rounding,
    #     )
    #     if (
    #         float_compare(
    #             self.product_qty, qty, precision_rounding=self.product_uom.rounding
    #         )
    #         != 0
    #     ):
    #         self.secondary_uom_qty = qty
    #
    # @api.onchange("secondary_uom_qty")
    # def _onchange_secondary_qty(self):
    #     if not self.secondary_uom_id:
    #         return
    #     # factor = self.secondary_uom_id.factor * self.product_uom.factor
    #     factor = self.secondary_uom_id.factor_inv
    #     qty = float_round(
    #         self.secondary_uom_qty * factor,
    #         precision_rounding=self.product_uom.rounding,
    #     )
    #     if (
    #             float_compare(
    #                 self.product_qty, qty, precision_rounding=self.product_uom.rounding
    #             )
    #             != 0
    #     ):
    #         self.product_qty = qty
    #
    # @api.onchange("product_qty")
    # def _onchange_product_qty_purchase_order_secondary_unit(self):
    #     if not self.secondary_uom_id:
    #         return
    #     # factor = self.secondary_uom_id.factor * self.product_uom.factor
    #     factor = self.secondary_uom_id.factor_inv
    #     # qty = float_round(
    #     #     self.product_qty / (factor or 1.0),
    #     #     precision_rounding=self.secondary_uom_id.uom_id.rounding,
    #     # )
    #     qty = float_round(
    #         self.product_qty / (factor or 1.0),
    #         precision_rounding=self.secondary_uom_id.rounding,
    #     )
    #     if (
    #         # float_compare(
    #         #     self.secondary_uom_qty,
    #         #     qty,
    #         #     precision_rounding=self.secondary_uom_id.uom_id.rounding,
    #         # )
    #             float_compare(
    #                 self.secondary_uom_qty,
    #                 qty,
    #                 precision_rounding=self.secondary_uom_id.rounding,
    #             )
    #         != 0
    #     ):
    #         self.secondary_uom_qty = qty
    #
    #
    # @api.onchange('price_subtotal')
    # def _onchange_purchase_price_subtotal(self):
    #     if self.price_subtotal and self.price_unit:
    #         self.product_qty = self.price_subtotal / self.price_unit
    #
    # @api.onchange('price_unit')
    # def _onchange_price_unit(self):
    #     if self.product_id.is_secondary_conversions:
    #         self.secondary_purchase_price = self.price_unit * self.secondary_uom_id.factor_inv
    #     else:
    #         self.secondary_purchase_price = self.price_unit
    #
    # @api.onchange('secondary_purchase_price')
    # def onchange_secondary_purchase_price(self):
    #     if self.product_id.is_secondary_conversions:
    #         factor = self.secondary_uom_id.factor_inv
    #         self.price_unit = self.secondary_purchase_price / factor



from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    @api.model
    def _get_fields_onchange_subtotal_model(self, price_subtotal, move_type, currency, company, date):
        _logger.warning("-----_get_fields_onchange------")
        ''' This method is used to recompute the values of 'amount_currency', 'debit', 'credit' due to a change made
        in some business fields (affecting the 'price_subtotal' field).

        :param price_subtotal:  The untaxed amount.
        :param move_type:       The type of the move.
        :param currency:        The line's currency.
        :param company:         The move's company.
        :param date:            The move's date.
        :return:                A dictionary containing 'debit', 'credit', 'amount_currency'.
        '''
        if move_type in self.move_id.get_outbound_types():
            sign = 1
        elif move_type in self.move_id.get_inbound_types():
            sign = -1
        else:
            sign = 1

        amount_currency = price_subtotal * sign
        to_force_exchange_rate = self.move_id.to_force_exchange_rate
        force_flag = to_force_exchange_rate != 0.0 and self.move_id.company_id.currency_id != self.move_id.currency_id
        if force_flag:
            balance = currency._force_convert(amount_currency, company.currency_id, company, to_force_exchange_rate)
        else:
            balance = currency._convert(amount_currency, company.currency_id, company, date or fields.Date.context_today(self))
        return {
            'amount_currency': amount_currency,
            'currency_id': currency.id,
            'debit': balance > 0.0 and balance or 0.0,
            'credit': balance < 0.0 and -balance or 0.0,
        }
    
    # @api.model_create_multi
    # def create(self, vals_list):
    #     # OVERRIDE
    #     ACCOUNTING_FIELDS = ('debit', 'credit', 'amount_currency')
    #     BUSINESS_FIELDS = ('price_unit', 'quantity', 'discount', 'tax_ids')

    #     for vals in vals_list:
    #         move = self.env['account.move'].browse(vals['move_id'])
    #         vals.setdefault('company_currency_id', move.company_id.currency_id.id)

    #         # Ensure balance == amount_currency in case of missing currency or same currency as the one from the company.
    #         currency_id = vals.get('currency_id') or move.company_id.currency_id.id
    #         if currency_id == move.company_id.currency_id.id:
    #             balance = vals.get('debit', 0.0) - vals.get('credit', 0.0)
    #             vals.update({
    #                 'currency_id': currency_id,
    #                 'amount_currency': balance,
    #             })
    #         else:
    #             vals['amount_currency'] = vals.get('amount_currency', 0.0)

    #         if move.is_invoice(include_receipts=True):
    #             currency = move.currency_id
    #             partner = self.env['res.partner'].browse(vals.get('partner_id'))
    #             taxes = self.new({'tax_ids': vals.get('tax_ids', [])}).tax_ids
    #             tax_ids = set(taxes.ids)
    #             taxes = self.env['account.tax'].browse(tax_ids)

    #             # Ensure consistency between accounting & business fields.
    #             if any(vals.get(field) for field in ACCOUNTING_FIELDS):
    #                 price_subtotal = self._get_price_total_and_subtotal_model(
    #                     vals.get('price_unit', 0.0),
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     currency,
    #                     self.env['product.product'].browse(vals.get('product_id')),
    #                     partner,
    #                     taxes,
    #                     move.move_type,
    #                 ).get('price_subtotal', 0.0)
                    
    #                 # Handle missing price_subtotal
    #                 if 'price_subtotal' in vals:
    #                     vals.update(self._get_fields_onchange_balance_model(
    #                         vals.get('quantity', 0.0),
    #                         vals.get('discount', 0.0),
    #                         vals['amount_currency'],
    #                         move.move_type,
    #                         currency,
    #                         taxes,
    #                         price_subtotal
    #                     ))
    #                 else:
    #                     _logger.warning("Price subtotal is missing in vals")

    #                 vals.update(self._get_price_total_and_subtotal_model(
    #                     vals.get('price_unit', 0.0),
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     currency,
    #                     self.env['product.product'].browse(vals.get('product_id')),
    #                     partner,
    #                     taxes,
    #                     move.move_type,
    #                 ))
    #             elif any(vals.get(field) for field in BUSINESS_FIELDS):
    #                 vals.update(self._get_price_total_and_subtotal_model(
    #                     vals.get('price_unit', 0.0),
    #                     vals.get('quantity', 0.0),
    #                     vals.get('discount', 0.0),
    #                     currency,
    #                     self.env['product.product'].browse(vals.get('product_id')),
    #                     partner,
    #                     taxes,
    #                     move.move_type,
    #                 ))
    #                 # Handle missing price_subtotal
    #                 if 'price_subtotal' in vals:
    #                     vals.update(self._get_fields_onchange_subtotal_model(
    #                         vals['price_subtotal'],
    #                         move.move_type,
    #                         currency,
    #                         move.company_id,
    #                         move.invoice_date,
    #                     ))
    #                 else:
    #                     _logger.warning("Price subtotal is missing in vals")

    #     lines = super(AccountMoveLine, self).create(vals_list)

    #     moves = lines.mapped('move_id')
    #     if self._context.get('check_move_validity', True):
    #         # Definir el contenedor
    #         container = {'records': moves}
    #         # Llamar a la función _check_balanced con el contenedor
    #         with moves._check_balanced(container):
    #             pass  # Esto es necesario para ejecutar el context manager correctamente
    #     moves._check_fiscalyear_lock_date()
    #     lines._check_tax_lock_date()
    #     moves._synchronize_business_models({'lineforce_flaif g_ids'})

    #     return lines


        
    @api.onchange('amount_currency')
    def _onchange_amount_currency(self):
        _logger.warning("-----_onchange_amount_------")
        for line in self:
            company = line.move_id.company_id
            to_force_exchange_rate = line.move_id.to_force_exchange_rate
            force_flag = to_force_exchange_rate != 0.0 and line.move_id.company_id.currency_id != line.move_id.currency_id
            if force_flag:
                balance = line.currency_id._force_convert(line.amount_currency, company.currency_id, company, to_force_exchange_rate)
            else:
                balance = line.currency_id._convert(line.amount_currency, company.currency_id, company, line.move_id.invoice_date or fields.Date.context_today(line))
            line.debit = balance if balance > 0.0 else 0.0
            line.credit = -balance if balance < 0.0 else 0.0

            if not line.move_id.is_invoice(include_receipts=True):
                continue

            line.update(line._get_fields_onchange_balance())
            line.update(line._get_price_total_and_subtotal())
            
    def _get_computed_price_unit(self):
        _logger.warning("-----_get_computed_price_unit------")
        ''' Helper to get the default price unit based on the product by taking care of the taxes
        set on the product and the fiscal position.
        :return: The price unit.
        '''
        self.ensure_one()

        if not self.product_id:
            return 0.0

        company = self.move_id.company_id
        currency = self.move_id.currency_id
        company_currency = company.currency_id
        product_uom = self.product_id.uom_id
        fiscal_position = self.move_id.fiscal_position_id
        is_refund_document = self.move_id.move_type in ('out_refund', 'in_refund')
        move_date = self.move_id.invoice_date or fields.Date.context_today(self)

        if self.move_id.is_sale_document(include_receipts=True):
            product_price_unit = self.product_id.lst_price
            product_taxes = self.product_id.taxes_id
        elif self.move_id.is_purchase_document(include_receipts=True):
            product_price_unit = self.product_id.standard_price
            product_taxes = self.product_id.supplier_taxes_id
        else:
            return 0.0
        product_taxes = product_taxes.filtered(lambda tax: tax.company_id == company)

        # Apply unit of measure.
        if self.product_uom_id and self.product_uom_id != product_uom:
            product_price_unit = product_uom._compute_price(product_price_unit, self.product_uom_id)

        # Apply fiscal position.
        if product_taxes and fiscal_position:
            product_taxes_after_fp = fiscal_position.map_tax(product_taxes)

            if set(product_taxes.ids) != set(product_taxes_after_fp.ids):
                flattened_taxes_before_fp = product_taxes._origin.flatten_taxes_hierarchy()
                if any(tax.price_include for tax in flattened_taxes_before_fp):
                    taxes_res = flattened_taxes_before_fp.compute_all(
                        product_price_unit,
                        quantity=1.0,
                        currency=company_currency,
                        product=self.product_id,
                        partner=self.partner_id,
                        is_refund=is_refund_document,
                    )
                    product_price_unit = company_currency.round(taxes_res['total_excluded'])

                flattened_taxes_after_fp = product_taxes_after_fp._origin.flatten_taxes_hierarchy()
                if any(tax.price_include for tax in flattened_taxes_after_fp):
                    taxes_res = flattened_taxes_after_fp.compute_all(
                        product_price_unit,
                        quantity=1.0,
                        currency=company_currency,
                        product=self.product_id,
                        partner=self.partner_id,
                        is_refund=is_refund_document,
                        handle_price_include=False,
                    )
                    for tax_res in taxes_res['taxes']:
                        tax = self.env['account.tax'].browse(tax_res['id'])
                        if tax.price_include:
                            product_price_unit += tax_res['amount']

        # Apply currency rate.
        if currency and currency != company_currency:
            to_force_exchange_rate = self.move_id.to_force_exchange_rate
            force_flag = to_force_exchange_rate != 0.0 and self.move_id.company_id.currency_id != self.move_id.currency_id
            if force_flag:
                product_price_unit = company_currency._force_convert(product_price_unit, company.currency_id, company, to_force_exchange_rate)
            else:            
                product_price_unit = company_currency._convert(product_price_unit, company.currency_id, company, move_date)

        return product_price_unit
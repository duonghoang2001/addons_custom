# -*- coding: utf-8 -*-

from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order' 

    @api.model
    def default_get(self, fields):
        """ Attached opportunity requests to new quotation """
        result = super(SaleOrder, self).default_get(fields)
        context = self._context
        if context and context.get('default_opportunity_id', 0):
            lead_id = context.get('default_opportunity_id')
            lead = self.env['crm.lead'].search([('id','=',lead_id)])
            order_lines = []
            if lead.id:
                for request_line in lead.request_ids:
                    order_lines.append((0, 0, {
                        'product_id': request_line.product_id,
                        'product_uom_qty': request_line.qty,
                        'price_unit': request_line.product_id.list_price
                    })) # link to a new record that need to be created
            
            result.update({
                'order_line': order_lines
            })

        return result
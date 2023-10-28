# -*- coding: utf-8 -*-

from odoo import models, fields


class CustomerRequest(models.Model):
    _name = 'crm.customer.request'
    _description = "Customer's Requests"

    product_id = fields.Many2one('product.template', string='Product', required=True)
    opportunity_id = fields.Many2one('crm.lead', string='Opportunity', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    description = fields.Char(string='Description')
    qty = fields.Float(string='Quantity', default=1)
    
    
    
    


    


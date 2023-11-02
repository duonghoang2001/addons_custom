# -*- coding: utf-8 -*-

from odoo import models, fields


class CustomerRequest(models.Model):
    _name = 'crm.customer.request'
    _order = 'create_date desc'
    _description = "Customer's Requests"
    _rec_name = 'opportunity_id'

    product_id = fields.Many2one(
        'product.template', string='Product', required=True, 
        help="Select product from database to request.")
    opportunity_id = fields.Many2one(
        'crm.lead', string='Opportunity', required=True, 
        help="Lead/Opportunity that request belongs to.")
    date = fields.Date(
        string='Date', required=True, default=fields.Date.context_today,
        help="Product request date.")
    description = fields.Char(string='Description')
    qty = fields.Float(string='Quantity', default=1)
    
    
    
    


    


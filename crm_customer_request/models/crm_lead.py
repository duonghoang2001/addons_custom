# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Lead(models.Model):
    _inherit = 'crm.lead'

    request_ids = fields.One2many('crm.customer.request', 'opportunity_id', string='Requests')
    total_sale = fields.Float(string='Total Sale', compute='_compute_total_sale', 
                              store=True)
    total_expected_revenue = fields.Monetary(string='Total Expected Revenue', 
                                             currency_field='company_currency',
                                             compute='_compute_total_expected_revenue',
                                             store=True)
    
    #@api.depends('crm_customer_request.quantity')
    def _compute_total_sale(self):
        self.total_sale = sum([request.quantity for request in self.request_ids])

    #@api.depends('crm_customer_request.quantity', 'crm_customer_request.product_id', 'product_id.list_price')
    def _compute_total_expected_revenue(self):
        revenues = [request.quantity * request.product_id.list_price for request in self.request_ids]
        self.total_expected_revenue = sum(revenues)
        

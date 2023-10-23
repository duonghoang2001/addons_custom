# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LeadExtend(models.Model):
    _inherit = 'crm.lead'

    request_ids = fields.One2many('crm.customer.request', string='Request IDs')
    total_sale = fields.Float(string='Total Sale', compute='_compute_total_sale', 
                              store=True)
    total_expected_revenue = fields.Monetary(string='Total Expected Revenue', 
                                             currency_field='company_currency',
                                             compute='_compute_total_expected_revenue',
                                             store=True)
    
    @api.depends('request_ids')
    def _compute_total_sale(self):
        self.total_sale = sum([quantity for quantity in self.mapped('request_ids.quantity')])

    @api.depends('request_ids')
    def _compute_total_expected_revenue(self):
        #FIXME: sum([quanity * list_price for quantity, list_price in self.mapped('request_ids)])
        # list_price from request_ids --> product_id --> list_price
        self.total_expected_revenue = sum([quantity for quantity in self.mapped('request_ids.quantity')])
        

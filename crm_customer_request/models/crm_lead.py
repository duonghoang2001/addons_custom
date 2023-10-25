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
    
    is_new_stage = fields.Boolean(string='Is New Stage?', compute='_compute_is_new_stage')
    
    #@api.depends('crm_customer_request.qty')
    def _compute_total_sale(self):
        for lead in self:
            lead.total_sale = sum([request.qty for request in lead.request_ids])

    #@api.depends('crm_customer_request.qty', 'crm_customer_request.product_id', 'product_id.list_price')
    def _compute_total_expected_revenue(self):
        for lead in self:
            revenues = [request.qty * request.product_id.list_price for request in lead.request_ids]
            lead.total_expected_revenue = sum(revenues)

    def _compute_is_new_stage(self):
        #FIXME: check whether current stage is 'New'
        for lead in self:
            new_stage_id = lead.env.ref('crm.stage_lead1').id
            record_id = lead.env.ref('crm.crm_lead_view_form').id
            print('Debug:', new_stage_id, record_id)
            lead.is_new_stage = new_stage_id == 1
    
        

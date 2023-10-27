# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Lead(models.Model):
    _inherit = ['crm.lead']

    request_ids = fields.One2many('crm.customer.request', 'opportunity_id', 
                                  string='Requests')
    total_sale = fields.Float(string='Total Sale', compute='_compute_total_sale', 
                              store=True)
    total_expected_revenue = fields.Monetary(string='Total Expected Revenue', 
                                             currency_field='company_currency',
                                             compute='_compute_total_expected_revenue',
                                             store=True)
    
    is_new_stage = fields.Boolean(string='Is New Stage?', compute='_compute_is_new_stage')
    
    @api.depends('request_ids.qty')
    def _compute_total_sale(self):
        for lead in self:
            lead.total_sale = sum([request.qty for request in lead.request_ids])

    @api.depends('request_ids.qty', 'request_ids.product_id', 'request_ids.product_id.list_price')
    def _compute_total_expected_revenue(self):
        for lead in self:
            revenues = [request.qty * request.product_id.list_price for request in lead.request_ids]
            lead.total_expected_revenue = sum(revenues)

    def _compute_is_new_stage(self):
        # Check whether current stage is 'New' (stage_id = 1)
        for lead in self:
            new_stage_id = lead.env.ref('crm.stage_lead1').id
            lead.is_new_stage = lead.stage_id.id == new_stage_id

            
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

    def create_quotaion_from_opporttunity(self):
        # Call the action_sale_quotations_new function
        action = self.env.ref('sale_crm.action_sale_quotations_new').read()[0]
        action_context = eval(action['context'])
        #print('debug', action)
        for lead in self:
            action_context.update({
                'default_opportunity_id': lead.opportunity_id.id,
                'default_opportunity_crm_lead_id': lead.opportunity_id.id,
                'default_order_line': [(0, 0, {
                    'product_id': line.product_id,
                    'product_uom_qty': line.qty,
                }) for line in lead.request_ids],
            })
            action['context'] = action_context

            action_copy = action.copy()
            self.env['sale.order'].create(action_copy['context'])  # create the quotation
            #print('debug: here')
        return True
        

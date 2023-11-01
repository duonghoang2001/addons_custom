# -*- coding: utf-8 -*-

import datetime
import json

from odoo import http
from odoo.http import request

class CrmCustomerRequest(http.Controller):
    @http.route('/crm_customer_request/crm_lead', auth='public', methods=['POST'], type='json')
    def create_lead(self, **kw):
        
        new_lead = {
            'email_from': kw['email'],
            'phone': kw['phone'],
            'description': kw['internal_notes'],
        }
        # Name
        new_lead['name'] = kw['name'] if kw['name'] else "%s's Opportunity" % kw['customer']
        # Customer: search for existing customer
        partner_id = request.env['res.partner'].search([('name', '=', kw['customer'])]).id
        if partner_id:
            new_lead['partner_id'] = partner_id
        # Expected closing date
        if kw['date_deadline']:
            new_lead['date_deadline'] = datetime.datetime.strptime(kw['date_deadline'], '%d/%m/%Y').date()
        
        # Requests
        new_lead['request_ids'] = []
        for i in range(len(kw['requests'])):
            product_id = request.env['product.template'].sudo().search(
                    [('name', '=', kw['requests'][i]['product'])], limit=1).id
            if product_id:
                new_lead['request_ids'].append(tuple({
                    'product_id': product_id,
                    'qty': kw['requests'][i]['quantity'],
                    'date': datetime.datetime.strptime(kw['requests'][i]['date'], '%d/%m/%Y').date()
                }))

        # Create lead
        new_lead_id = request.env['crm.lead'].sudo().create(new_lead).id
        print('Created Lead:', request.env['crm.lead'].sudo().search([('id', '=', new_lead_id)]))

        return json.dumps({'Result': 'Completed'}) 

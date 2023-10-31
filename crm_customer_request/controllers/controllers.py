# -*- coding: utf-8 -*-

import datetime
import json

from odoo import http
from odoo.http import request

class CrmCustomerRequest(http.Controller):
    @http.route('/crm_customer_request/crm_lead', auth='public', methods=['POST'], type="json")
    def create_lead(self, **kw):
        new_lead = {
            'email_from': kw['email'],
            'phone': kw['phone'],
            'description': kw['internal_notes'],
        }
        # Name
        new_lead['name'] = kw['name'] if kw['name'] else "%s's Opportunity" % kw['customer']
        # Customer: search for existing customer, else, create new customer
        partner_id = request.env['res.partner'].search([('name', '=', kw['customer'])]).id
        if partner_id:
            new_lead['partner_id'] = partner_id
        else:
            request.env['res.partner'].sudo().name_create(kw['customer'])
            new_lead['partner_id'] = request.env['res.partner'].search(
                [('name', '=', kw['customer'])]).id
        # Expected closing date
        try:
            expected_closing = datetime.datetime.strptime(kw['date_deadline'], '%d/%m/%Y').date()
            new_lead['date_deadline'] = expected_closing
        except TypeError:
            pass
        except ValueError:
            pass
        # Requests
        new_lead['request_ids'] = []
        for i in range(len(kw['requests'])):
            product_id = request.env['product.template'].sudo().search(
                    [('name', '=', kw['requests'][i]['product'])], limit=1).id
            if product_id:
                new_lead['request_ids'].append({
                    'product_id': product_id,
                    'qty': kw['requests'][i]['quantity'],
                })
                try:
                    date = datetime.datetime.strptime(kw['requests'][i]['date'], '%d/%m/%Y').date()
                    new_lead['request_ids'][-1]['date'] = date
                except TypeError:
                    pass
                except ValueError:
                    pass
        # Create lead
        request.env['crm.lead'].sudo().create([new_lead])

        return json.dumps({"result":"Success"}) 

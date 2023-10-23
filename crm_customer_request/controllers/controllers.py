# -*- coding: utf-8 -*-
# from odoo import http


# class CrmCustomerRequest(http.Controller):
#     @http.route('/crm_customer_request/crm_customer_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_customer_request/crm_customer_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_customer_request.listing', {
#             'root': '/crm_customer_request/crm_customer_request',
#             'objects': http.request.env['crm_customer_request.crm_customer_request'].search([]),
#         })

#     @http.route('/crm_customer_request/crm_customer_request/objects/<model("crm_customer_request.crm_customer_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_customer_request.object', {
#             'object': obj
#         })

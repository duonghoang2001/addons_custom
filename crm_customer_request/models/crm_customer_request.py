# -*- coding: utf-8 -*-

from odoo import models, fields


class CustomerRequest(models.Model):
    _name = 'crm.customer.request'
    _description = "Customer's Requests"

    product_id = fields.Many2one('product.template', string='Product', required=True)
    opportunity_id = fields.Many2one('crm.lead', string='Opportunity', required=True)
    date = fields.Date(required=True, default=fields.Date.today)
    description = fields.Text()
    quantity = fields.Float(default=1)


    


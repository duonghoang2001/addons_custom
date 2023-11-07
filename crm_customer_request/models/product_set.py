# -*- coding: utf-8 -*-

from odoo import api, fields, models

# We want to _inherits from the parent model and we add some fields
# in the child object
class ProductSet(models.Model):
    _name = 'product.set'
    _inherits = {'product.template': 'product_template_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Set'

    product_template_id = fields.Many2one(
        'product.template', string='Product Template', required=True, 
        ondelete='cascade', help="For Delegation Inheritance.")
    bundle_ok = fields.Boolean(string='Can be Bundled?', default=True)
    discount = fields.Float(string='Discount Amount', default=0)
    discount_rate = fields.Float(
        string='Discount Rate', compute='_compute_discount_percentage')
    discount_price = fields.Float(
        string='Discounted Price', compute='_compute_discount_price',
        help="It's more economical to buy listed products together instead of buying them individually.")
    opportunity_id = fields.Many2one(
        'crm.lead', string='Related Opportunity'
    )
    
    @api.onchange('discount', 'list_price')
    def _compute_discount_percentage(self):
        for record in self:
            record.discount_rate = record.discount / record.list_price if self.discount > 0 else 0
    
    @api.onchange('discount', 'list_price')
    def _compute_discount_price(self):
        for record in self:
            record.discount_price = record.list_price - record.discount

    def action_open_label_layout(self):
        action = self.env['ir.actions.act_window']._for_xml_id('product.action_open_label_layout')
        action['context'] = {'default_product_tmpl_ids': self.ids}
        return action

    def open_pricelist_rules(self):
        self.ensure_one()
        domain = ['|',
            ('product_tmpl_id', '=', self.product_template_id.id),
            ('product_id', '=', self.id)]
        return {
            'name': _('Price Rules'),
            'view_mode': 'tree,form',
            'views': [(self.env.ref('product.product_pricelist_item_tree_view_from_product').id, 'tree'), (False, 'form')],
            'res_model': 'product.pricelist.item',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            'context': {
                'default_product_id': self.id,
                'default_applied_on': '1_product',
            }
        }
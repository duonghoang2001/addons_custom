# -*- coding: utf-8 -*-

from odoo import models, fields

# We want to _inherits from the parent model and we add some fields
# in the child object
class ProductSet(models.Model):
    _name = 'product.set'
    _inherits = {'product.template': 'product_template_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Product Set'

    product_template_id = fields.Many2one(
        'product.template', string='Related Product', required=True, 
        ondelete='cascade', help="Product that the Set related to.")
    bundle_ok = fields.Boolean(string='Can be Bundled?', default=True)
    qty = fields.Integer(string='Quantity', default=1, help="Quantity of products contained in the set.")
    opportunity_id = fields.Many2one(
        'crm.lead', string='Related Opportunity'
    )
    
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
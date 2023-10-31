# -*- coding: utf-8 -*-

import base64
import datetime
import xlrd
from xlsxwriter import Workbook
from io import BytesIO
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.modules.module import get_module_resource

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
    # Stage
    is_new_stage = fields.Boolean(string='Is New Stage?', compute='_compute_is_new_stage')
    # Excel file upload/download
    excel_file = fields.Binary(string='Upload File')
    excel_file_name = fields.Char(string='Filename')
    excel_template = fields.Many2one('ir.attachment', string='Request File Template', compute='_compute_excel_template')
    excel_data = fields.Many2one('ir.attachment', string='Request Data', compute='_compute_excel_data')
    
    @api.depends('request_ids.qty')
    def _compute_total_sale(self):
        for lead in self:
            lead.total_sale = sum([request.qty for request in lead.request_ids])

    @api.depends('request_ids.qty', 'request_ids.product_id.list_price')
    def _compute_total_expected_revenue(self):
        for lead in self:
            revenues = [request.qty * request.product_id.list_price for request in lead.request_ids]
            lead.total_expected_revenue = sum(revenues)

    def _compute_is_new_stage(self):
        # Check whether current stage is 'New' (stage_id = 1)
        for lead in self:
            new_stage_id = lead.env.ref('crm.stage_lead1').id
            lead.is_new_stage = lead.stage_id.id == new_stage_id

    def _compute_excel_template(self):
        file_path = get_module_resource('crm_customer_request', 'static', 'requests_template.xlsx')
        self.excel_template = self.env['ir.attachment'].create({
            'name': 'excel_template',
            'type': 'binary',
            'datas': base64.b64encode(open(file_path, 'rb').read()),
            'res_id': self.id
        })

    @api.depends('request_ids.description', 'request_ids.date', 'request_ids.qty', 
                 'request_ids.product_id.name', 'request_ids.opportunity_id.name')
    def _compute_excel_data(self):
        # Save as file object
        in_memory_fp = BytesIO()
        with Workbook(in_memory_fp) as workbook:
            worksheet = workbook.add_worksheet()
            headers = ['Product', 'Opportunity', 'Date (dd/mm/YYYY)', 'Description', 'Quantity']
            worksheet.write_row(row=0, col=0, data=headers)
            for i in range(len(self.request_ids)):
                request = self.request_ids[i]
                row = [request.product_id.name, 
                       request.opportunity_id.name, 
                       request.date.strftime('%d/%m/%Y'), 
                       request.description if request.description else '', 
                       request.qty]
                worksheet.write_row(row=i + 1, col=0, data=row)

        in_memory_fp.seek(0,0)
        self.excel_data = self.env['ir.attachment'].create({
            'name': 'excel_requests',
            'type': 'binary',
            'datas': base64.b64encode(in_memory_fp.read()),
            'res_id': self.id
        })

    def download_file(self, attachment):
        return {
            'type': 'ir.actions.act_url',
            'name': 'download_file',
            'url': '/web/image?model=ir.attachment&field=datas&id=%s&filename=%s' 
                        % (attachment.id, attachment.name),
            'target': 'new',
        }

    def download_template(self):
        return self.download_file(self.excel_template)
    
    def download_requests(self):
        return self.download_file(self.excel_data)
    
    def import_excels(self):
        # Read uploaded excel file
        try:
            file_data = base64.b64decode(self.excel_file)
            book = xlrd.open_workbook(file_contents=file_data)
        except xlrd.biffh.XLRDError:
            raise UserError('Only Excel files are supported.')
        # Extract data from excel file
        for sheet in book.sheets():
            try:
                line_vals = []
                for row in range(sheet.nrows):
                    if row >= 1:
                        row_values = sheet.row_values(row)
                        vals = self.create_request_entry(row_values)
                        line_vals.append((0, 0, vals))

                if line_vals:
                    self.update({
                        'request_ids': line_vals
                    })
            except IndexError:
                pass

    def create_request_entry(self, record):
        # Search for product ID using product's name
        product_id = self.env['product.template'].search([('name', '=', record[0])], limit=1).id
        # Only add valid fields, invalid ones would be left as default values
        if product_id:
            request_line = {
                'product_id': product_id
            }
            if record[1]:
                try:
                    date = datetime.datetime.strptime(record[1], '%d/%m/%Y').date()
                    request_line['date'] = date
                except ValueError:
                    pass
                except TypeError:
                    pass
            if record[2]:
                request_line['description'] = record[2]
            if type(record[3]) in (int, float):
                request_line['qty'] = record[3]

            return request_line
        else:
            error_message = _("Product '%s' is not available!", record[0])
            raise ValidationError(error_message)
        
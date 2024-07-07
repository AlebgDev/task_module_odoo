from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import requests
import xml.etree.ElementTree as ET


import logging

_logger = logging.getLogger(__name__)

class TaskModel(models.Model):
    _name = "task.model"
    _rec_name = "task_name"
    _check_company_auto = True

    state = fields.Selection([('waiting','Waiting'),('process','Process'),('closed','Closed')], string="State", default="waiting")
    task_name = fields.Char(string="Task Name", copy=False, tracking=True, required=True)
    task_description = fields.Char(string="Task Description", copy=False, tracking=True, required=True)
    due_date = fields.Date(string="Due date")
    tag_ids = fields.Many2many("task.tag", string="Tag")
    priority= fields.Selection([('0','Low'),('1','Normal'),('2','High'),('3','Important')], string='Priority', required=True)

    def button_send_to_odoo_17(self):
        connect_url = 'http://localhost:8069/task/connect'
        send_url = 'http://192.168.0.102:17000/xmlrpc/2/object'
        
        db = 'odoo_17'
        username = 'test'
        password = '53a8bc8a72a59dad367e6deb469a24714e65645b'
        model = 'task.model'
        method = 'create'
        fields_data = {
            'state': self.state,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'priority': self.priority,
        }

        try:
            # Paso 1: Conexión y obtención del UID
            connect_response = requests.post(connect_url, json={})
            if connect_response.status_code != 200:
                raise UserError('Error in connection: {}'.format(connect_response.status_code))
            
            connect_result = connect_response.json()
        
            if connect_result['result']['status'] != 'success':
                raise UserError('Failed to connect: {}'.format(connect_result.get('message', 'No message')))
            
            # Extraer el UID del XML en la respuesta
            xml_response = connect_result['result']['response']
            root = ET.fromstring(xml_response)
            uid = root.find('.//value/int').text

            _logger.info('UID obtained: %s', uid)
            
            # Paso 2: Construcción del cuerpo XML y envío de datos
            method_call = ET.Element('methodCall')
            method_name = ET.SubElement(method_call, 'methodName')
            method_name.text = 'execute'

            params = ET.SubElement(method_call, 'params')

            for param_value in [db, uid, password, model, method]:
                param = ET.SubElement(params, 'param')
                value = ET.SubElement(param, 'value')
                value_type = ET.SubElement(value, 'string')
                value_type.text = str(param_value)

            param = ET.SubElement(params, 'param')
            struct = ET.SubElement(param, 'struct')

            for field, value in fields_data.items():
                member = ET.SubElement(struct, 'member')
                name = ET.SubElement(member, 'name')
                name.text = field
                value_elem = ET.SubElement(member, 'value')
                value_string = ET.SubElement(value_elem, 'string')
                value_string.text = str(value)

            body = ET.tostring(method_call, encoding='unicode')
            headers = {'Content-Type': 'text/xml'}

            send_response = requests.post(send_url, data=body, headers=headers)
            if send_response.status_code == 200:
                _logger.info('Data sent successfully: %s', send_response.text)
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'Data sent successfully.',
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                _logger.warning('Data sending failed with status code: %s', send_response.status_code)
                raise UserError('Data sending failed with status code: {}'.format(send_response.status_code))
        
        except requests.exceptions.RequestException as e:
            _logger.error('Exception during connection: %s', str(e))
            raise UserError('Exception during connection: {}'.format(str(e)))
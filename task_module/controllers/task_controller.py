from odoo import http
from odoo.http import request
import xml.etree.ElementTree as ET
import requests

import logging

_logger = logging.getLogger(__name__)

class TaskController(http.Controller):

    @http.route('/task/connect', type='json', auth='none', methods=['POST'], csrf=False)
    def connect_api_xmlrpc(self, **kwargs):
        url = 'http://192.168.0.102:17000/xmlrpc/2/common'
        username = kwargs.get('username', 'test')
        password = kwargs.get('password', 'test')
        db = kwargs.get('db', 'odoo_17')

        body = f"""
        <methodCall>
            <methodName>login</methodName>
            <params>
                <param><value><string>{db}</string></value></param>
                <param><value><string>{username}</string></value></param>
                <param><value><string>{password}</string></value></param>
            </params>
        </methodCall>
        """
        try:
            response = requests.post(url, data=body)
            if response.status_code == 200:
                _logger.info('Connection successful: %s', response.text)
                return {'status': 'success', 'response': response.text}
            else:
                _logger.warning('Connection failed with status code: %s', response.status_code)
                return {'status': 'failed', 'message': ' failed with status code: {}'.format(response.status_code)}
        except Exception as e:
            _logger.error('Exception during connection: %s', str(e))
            return {'status': 'error', 'message': str(e)}

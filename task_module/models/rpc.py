import xmlrpc.client

url='http://localhost:17000'
db='odoo_17'
username='test'
password='53a8bc8a72a59dad367e6deb469a24714e65645b'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())

uid = common.authenticate(db, username, password, {})
print(uid)
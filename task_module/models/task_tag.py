from odoo import api, fields, models

class TaskTag(models.Model):
    _name = "task.tag"
    _rec_name = "name"
    _order = "name desc"
    _check_company_auto = True

    name = fields.Char(string="Name", copy=False, tracking=True, required=True)
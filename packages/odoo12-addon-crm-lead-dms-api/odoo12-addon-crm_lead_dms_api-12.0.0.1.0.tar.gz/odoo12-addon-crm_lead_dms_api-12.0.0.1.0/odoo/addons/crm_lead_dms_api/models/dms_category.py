from odoo import models, fields


class Category(models.Model):
    _inherit = "dms.category"

    code = fields.Char(string="code")

from odoo import models, api, fields
import secrets


class Lead(models.Model):
    _inherit = "crm.lead"

    token = fields.Char(string="Token", unique=True, index=True)

    @api.model
    def create(self, vals):
        vals["token"] = self.generate_unique_token()
        return super().create(vals)

    def generate_unique_token(self):
        token_length = 32
        existing_lead = True
        token = ""
        while existing_lead:
            token = secrets.token_urlsafe(token_length)
            existing_lead = self.search([("token", "=", token)])
        return token

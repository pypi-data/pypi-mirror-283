from . import models
from odoo import api, SUPERUSER_ID


def post_install_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    crm_lead = env["crm.lead"]
    crm_leads = crm_lead.search([])
    for lead in crm_leads:
        if not lead.token:
            lead.write({"token": lead.generate_unique_token()})

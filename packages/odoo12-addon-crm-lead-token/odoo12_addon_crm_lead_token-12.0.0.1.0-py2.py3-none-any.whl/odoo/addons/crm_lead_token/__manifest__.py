# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "SomItCoop ODOO CRM Lead Token",
    "version": "12.0.0.1.0",
    "depends": ["crm"],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Customer Relationship Management",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Generate unique token for crm.lead
    """,
    "data": [
        "views/crm_lead_views.xml",
    ],
    "application": False,
    "installable": True,
    "post_init_hook": "post_install_hook",
}

# Copyright 2023-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "SomItCoop Odoo crm with category to mark the required documents",
    "version": "12.0.0.1.0",
    "depends": ["dms", "crm"],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Customer Relationship Management",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        Category to mark the required documents on crm.lead
    """,
    "data": [
        "views/crm_lead_views.xml",
    ],
    "application": False,
    "installable": True,
}

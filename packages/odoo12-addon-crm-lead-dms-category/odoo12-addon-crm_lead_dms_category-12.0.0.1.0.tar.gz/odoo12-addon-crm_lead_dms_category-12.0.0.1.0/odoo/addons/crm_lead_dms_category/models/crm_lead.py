# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    dms_category_ids = fields.Many2many(
        "dms.category",
        "crm_lead_dms_category_rel",
        "lead_id",
        "dms_category_id",
        string="Category",
        help="Category to mark the required documents",
    )

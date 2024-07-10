# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component

import logging


_logger = logging.getLogger(__name__)


class CrmLeadAPI(Component):
    _name = "crm.lead.api.service"
    _inherit = "base.rest.service"
    _usage = "crm-lead"
    _collection = "api_common_base.services"
    _description = """
    Knowledge Categories API
    Access to the crm lead documents with GET method
    """

    @restapi.method(
        [(["/documents-required/<string:crm_lead_token>"], "GET")],
    )
    def get_document_required(self, crm_lead_token):
        crm_leads = self.env["crm.lead"].search([("token", "=", str(crm_lead_token))])
        result = []
        if crm_leads:
            crm_lead = crm_leads[0]
            if crm_lead.partner_id:
                for dms_category_id in crm_lead.dms_category_ids:
                    documents = self.env["ir.attachment"].search(
                        [
                            ("res_model", "=", "res.partner"),
                            ("res_id", "=", crm_lead.partner_id.id),
                        ]
                    )
                    if documents:
                        dms_file = self.env["dms.file"].search(
                            [
                                ("category_id", "=", dms_category_id.id),
                                ("attachment_id", "in", documents.ids),
                            ]
                        )

                    result.append(
                        {
                            "crm_lead_id": crm_lead.id,
                            "crm_lead_token": crm_lead.token,
                            "document_category": dms_category_id.code,
                            "document_id": dms_file[0].id
                            if documents and dms_file
                            else False,
                            "document_exit": True if documents and dms_file else False,
                        }
                    )
        _logger.debug(result)
        return request.make_json_response(result)

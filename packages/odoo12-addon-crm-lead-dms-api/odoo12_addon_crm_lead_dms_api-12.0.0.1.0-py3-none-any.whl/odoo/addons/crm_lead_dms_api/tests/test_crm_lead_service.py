import json
from odoo.addons.api_common_base.tests.common_service import APICommonBaseRestCase


class TestCrmLead(APICommonBaseRestCase):
    def setUp(self):
        super().setUp()
        self.Lead = self.env["crm.lead"]
        self.Category = self.env["dms.category"]
        self.category = self.Category.create({"name": "Prueba", "code": "test"})
        self.partner = self.env.ref("base.partner_admin")
        self.lead = self.Lead.create(
            {
                "name": "Prueba",
                "partner_id": self.partner.id,
                "dms_category_ids": [(6, 0, [self.category.id])],
            }
        )
        self.url = f"/api/crm-lead/documents-required/{self.lead.token}"

    def test_check_document_requirement(self):
        """
        Test check document requirement
        """
        response = self.http_get(self.url)
        self.assertEquals(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        for docu in content:
            self.assertIn("crm_lead_id", docu)
            self.assertIn("crm_lead_token", docu)
            self.assertIn("document_category", docu)
            self.assertIn("document_id", docu)
            self.assertIn("document_exit", docu)

            self.assertEquals(docu.get("crm_lead_id"), self.lead.id)
            self.assertEquals(docu.get("crm_lead_token"), self.lead.token)
            self.assertEquals(docu.get("document_category"), self.category.code)
            self.assertEquals(docu.get("document_id"), False)
            self.assertEquals(docu.get("document_exit"), False)

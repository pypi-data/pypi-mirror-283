from odoo.tests import common


class TestLead(common.SavepointCase):
    def setUp(self):
        super().setUp()
        self.lead_model = self.env["crm.lead"]

    def test_generate_unique_token(self):
        # Crear un lead para asegurarse de que haya al menos uno en la base de datos
        self.lead_model.create({"name": "Lead de prueba"})

        # Generar un token único
        token = self.lead_model.generate_unique_token()

        # Comprobar que el token se ha generado correctamente
        self.assertTrue(token)
        self.assertIsInstance(token, str)

        # Comprobar que no hay ningún otro lead con el mismo token
        leads_with_same_token = self.lead_model.search_count([("token", "=", token)])
        self.assertEqual(leads_with_same_token, 0)

    def test_create_lead(self):
        # Crear un lead sin proporcionar token
        lead = self.lead_model.create({"name": "Nuevo lead"})

        # Comprobar que el lead se ha creado correctamente
        self.assertTrue(lead)
        self.assertIsInstance(lead.token, str)
        self.assertTrue(lead.token)

        # Comprobar que no hay ningún otro lead con el mismo token
        leads_with_same_token = self.lead_model.search_count(
            [("token", "=", lead.token)]
        )
        self.assertEqual(leads_with_same_token, 1)

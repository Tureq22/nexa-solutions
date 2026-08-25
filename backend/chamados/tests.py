from rest_framework import status
from rest_framework.test import APITestCase


class ChamadoTests(APITestCase):

    def test_criar_chamado_sem_titulo(self):
        dados = {
            "titulo": "",
            "descricao": "Chamado sem título",
            "status": "ABERTO",
        }

        response = self.client.post("/api/chamados/", dados, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", response.data)
    
    
from django.urls import reverse
from rest_framework import status as http_status
from rest_framework.test import APITestCase

from .models import Chamado

class FiltroChamadosporStatusTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("chamado-list-create")

        Chamado.objects.create(titulo="Impressora sem tinta", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="VPN fora do ar", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="Troca de monitor", status=Chamado.Status.EM_ANDAMENTO)
        Chamado.objects.create(titulo="Reset de Senha", status=Chamado.Status.CONCLUIDO)

    def test_sem_filtro_retorna_todos_os_chamados(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, http_status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 2)
        for chamado in resposta.data:
            self.assertEqual(chamado["status"], Chamado.Status.ABERTO)

    def test_filtra_chamados_em_andamento(self):
        resposta = self.client.get(self.url, {"status": "EM_ANDAMENTO"})

        self.assertEqual(resposta.status_code, http_status.HTTP_200_OK)        
        self.assertEqual(len(resposta.data), 1)
        self.assertEqual(resposta.data[0]["titulo"], "Troca de monitor")

    def test_filtra_chamados_concluidos(self):
        resposta = self.client.get(self.url, {"status": "CONCLUIDO"})

        self.assertEqual(resposta.status_code, http_status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)
        self.assertEqual(resposta.data[0]["status"], Chamado.Status.CONCLUIDO)

    def test_filtro_aceita_valor_em_minusculo(self):
        resposta = self.client.get(self.url, {"status": "aberto"})

        self.assertEqual(resposta.status_code, http_status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 2)

    def test_status_invalido_retorna_400(self):
        resposta = self.client.get(self.url, {"status": "CANCELADO"})

        self.assertEqual(resposta.status_code, http_status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", resposta.data)

    def test_status_vazio_retorna_todos_os_chamados(self):
        resposta = self.client.get(self.url, {"status": ""})

        self.assertEqual(resposta.status_code, http_status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 4)
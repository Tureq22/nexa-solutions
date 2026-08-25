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

                
        
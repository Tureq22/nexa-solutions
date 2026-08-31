from django.db.models import Count, Q
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chamado
from .serializers import ChamadoSerializer


class ChamadoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria chamados.

    Limitações intencionais:
    - Não filtra chamados por status.
    - Não oferece indicadores.
    - Não há tratamento adicional para parâmetros inválidos.
    """

    queryset = Chamado.objects.all().order_by("-criado_em")
    serializer_class = ChamadoSerializer

def get_queryset(self):
    queryset = super().get_queryset()
    status = self.request.query_params.get("status")

    if status is None or status.strip() == "":
        return queryset

    status = status.strip().upper()

    if status not in Chamado.Status.values:
        raise ValidationError(
            {
                "status": [
                    "Status inválido. Valores aceitos: "
                    + ", ".join(Chamado.Status.values)
                    + "."
                ]
            }
        )
    return queryset.filter(status=status)


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer

class IndicadoresView(APIView):
    """
    Retorna os totais de chamados por status.

        GET /api/indicadores/
    """

    def get(self, request):
        indicadores = Chamado.objects.aggregate(
            total=Count("id"),
            abertos=Count("id", filter=Q(status=Chamado.Status.ABERTO)),
            em_andamento=Count("id", filter=Q(status=Chamado.Status.EM_ANDAMENTO)),
            concluidos=Count("id", filter=Q(status=Chamado.Status.CONCLUIDO)),
        )

        return Response(indicadores)
from rest_framework import generics
from rest_framework.exceptions import ValidationError

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
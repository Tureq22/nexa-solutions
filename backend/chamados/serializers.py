from rest_framework import serializers

from .models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado

        fields = [
            "id",
            "titulo",
            "descricao",
            "status",
            "criado_em",
            "atualizado_em",
        ]

        read_only_fields = [
            "id",
            "criado_em",
            "atualizado_em",
        ]
        extra_kwargs = {
            "titulo": {
                "required": True,
                "allow_blank": False,
                "error_messages": {
                    "required": "O título do chamado é obrigatório.",
                    "blank": "O título do chamado não pode ficar em branco.",
                    "null": "O título do chamado é obrigatório.",
                },
            },
        }
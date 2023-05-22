from rest_framework import serializers
from django.utils import timezone
from agenda.models import Agendamento

class AgendamentoUteis(serializers.Serializer):
    data_horario_disponivel = serializers.DateTimeField()


class AgendamentoAgendado(serializers.ModelSerializer):

    class Meta:
        model = Agendamento
        fields = ["id", "data_horario"]
        

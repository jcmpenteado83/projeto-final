from rest_framework import serializers
from django.utils import timezone
from agenda.models import Agendamento
from datetime import timedelta
from agenda.functions import horasuteis

class AgendamentoUteis(serializers.Serializer):
    data_horario_disponivel = serializers.DateTimeField()

   
class AgendamentoAgendado(serializers.ModelSerializer):

    class Meta:
        model = Agendamento
        fields = ["id", "data_horario"]
        
    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Agendamento não pode ser feito no passado")
        return value

    def validate(self, attrs):
        data_horario = attrs.get("data_horario", "")
        query = Agendamento.objects.filter(data_horario__day=data_horario.date().day, disponivel=False)
        hora = data_horario.time()
        horas = hora.strftime('%H:%M:%S')
        date_str = data_horario.strftime('%Y-%m-%d')
        hu = horasuteis(date_str)
        
        if horas not in hu:
            raise serializers.ValidationError("Os agendamentos ocorrem a partir das 09:00 e com intervalo de 30 minutos. Consulte os horários disponíveis.")

        for i in query:
            if i.data_horario == data_horario:
                raise serializers.ValidationError("Horário já utilizado para a data solicitada! Consulte os horários disponíveis.")
                        
        return attrs

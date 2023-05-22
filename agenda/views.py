from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime, timezone
from rest_framework.decorators import api_view
from agenda.serializers import AgendamentoUteis, AgendamentoAgendado
from agenda.models import Agendamento
from rest_framework.response import Response


@api_view(http_method_names=["GET"])
def horarios_list(request):
    if request.method == "GET":
        data = request.query_params.get("data")
        hd = horariosdisponiveis(data)
        serializer = AgendamentoUteis(hd, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(http_method_names=["POST", "GET"])
def agendar_horario(request):
    if request.method == "POST":
        serializer = AgendamentoAgendado(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    if request.method == "GET":
        data = request.query_params.get("data")
        obj = Agendamento.objects.filter(disponivel=False,data_horario__date=data)
        serializer = AgendamentoAgendado(obj, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(http_method_names=["DELETE"])
def agendamento_detail(request,id):
    obj = get_object_or_404(Agendamento, id=id)
    if request.method == "DELETE":
        obj.disponivel = True
        obj.save()
        return Response(status=204)


def horariosdisponiveis(data):
    qry = Agendamento.objects.filter(disponivel=False,data_horario__date=data)
    h = [ '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00', '17:00:00', '17:30:00']
    hu = []
    for i in h:
        horarios = {}
        horarios["data_horario_disponivel"] = data + 'T' + i
        hu.append(horarios)    
    for a in qry:
        hora_qry = a.data_horario.strftime('%H:%M:%S')
        for e in hu:
            hora = datetime.fromisoformat(e["data_horario_disponivel"]).time()
            horas = hora.strftime('%H:%M:%S')
            if hora_qry == horas:
                hu.remove(e)
    return hu

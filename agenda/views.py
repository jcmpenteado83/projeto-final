from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from agenda.serializers import AgendamentoUteis, AgendamentoAgendado
from agenda.models import Agendamento
from rest_framework.response import Response
from agenda.functions import horariosdisponiveis


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
        data_param = request.query_params.get("data")
        if data_param:
            obj = Agendamento.objects.filter(disponivel=False,data_horario__date=data_param)
            serializer = AgendamentoAgendado(obj, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            obj = Agendamento.objects.filter(disponivel=False)
            serializer = AgendamentoAgendado(obj, many=True)
            return JsonResponse(serializer.data, safe=False)


@api_view(http_method_names=["GET", "DELETE"])
def agendamento_detail(request,id):
    obj = get_object_or_404(Agendamento, id=id)
    if request.method == "GET":
        serializer = AgendamentoAgendado(obj)
        return JsonResponse(serializer.data, status=200)
    if request.method == "DELETE":
        obj.disponivel = True
        obj.save()
        return Response(status=204)

from agenda.models import Agendamento
from datetime import date, datetime


def horasuteis(data):
    to_date = datetime.fromisoformat(data).date()
    dia_semana = date.weekday(to_date)
    if dia_semana != 5 and dia_semana != 6:
        hu = [ '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00', '17:00:00', '17:30:00']
    elif dia_semana == 5:
        hu = [ '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00']
    else:
        hu = []
    return hu


def horariosdisponiveis(data):
    qry = Agendamento.objects.filter(disponivel=False,data_horario__date=data)
    h = horasuteis(data)
    hd = []
    for i in h:
        horarios = {}
        horarios["data_horario_disponivel"] = data + 'T' + i
        hd.append(horarios)    
    for a in qry:
        hora_qry = a.data_horario.strftime('%H:%M:%S')
        for e in hd:
            hora = datetime.fromisoformat(e["data_horario_disponivel"]).time()
            horas = hora.strftime('%H:%M:%S')
            if hora_qry == horas:
                hd.remove(e)
    return hd

from django.urls import path
from agenda.views import horarios_list, agendar_horario, agendamento_detail

urlpatterns = [
    path('horarios/', horarios_list),
    path('agendar/', agendar_horario),
    path('agendar/<int:id>/', agendamento_detail),

]

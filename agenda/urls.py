from django.urls import path
from agenda.views import horarios_list, agendar_horario, agendamento_detail

urlpatterns = [
    path('horarios/', horarios_list),
    path('agendamentos/', agendar_horario),
    path('agendamentos/<int:id>/', agendamento_detail),

]

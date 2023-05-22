from django.db import models

class Agendamento(models.Model):
    data_horario = models.DateTimeField()
    disponivel = models.BooleanField(default=False)


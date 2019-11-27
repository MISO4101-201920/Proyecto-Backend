from activities.views import *
from django.urls import path
from activities.views import CalificarAPI, MarcaApi, intentos_max
app_name = 'activities'


app_name = 'marca'
# add url path to the API
urlpatterns = [
    path('marca', MarcaView.as_view(), name='marca'),
    path('reports/<int:contentpk>', reports, name='reports'),
    path('respuestaOpcionMultiple/', RespuestaSeleccionMultipleView.as_view()),
    path('preguntaOpcionMultiple/<int:marca>/', DetailPreguntaSeleccionMultiple.as_view()),
    path('calificacion', CalificarAPI.as_view(), name='calificacion'),
    path('generate-question-multiple-choice', CreatePreguntaSeleccionMultiple.as_view(), name='pregunta seleccion multiple '),
    path('generate-open-question', CreatePreguntaAbierta.as_view(), name='pregunta abierta '),
    path('marca', MarcaApi.as_view(), name='marca'),
    path('ultimo_intento', intentos_max)
]
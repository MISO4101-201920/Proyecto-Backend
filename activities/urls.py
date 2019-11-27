from activities.views import *
from django.urls import path
from activities.views import CalificarAPI, MarcaApi, intentos_max, PreguntaFoVView, GetPausesView, GetPreguntaAbierta
app_name = 'activities'


app_name = 'marca'
# add url path to the API
urlpatterns = [
    path('marca', MarcaView.as_view(), name='marca'),
    path('reports/<int:contentpk>', reports, name='reports'),
    path('respuestaOpcionMultiple/', RespuestaSeleccionMultipleView.as_view()),
    path('preguntaOpcionMultiple/<int:marca>/',
         DetailPreguntaSeleccionMultiple.as_view()),
    path('calificacion', CalificarAPI.as_view(), name='calificacion'),
    path('generate-question-multiple-choice',
         CreatePreguntaSeleccionMultiple.as_view(), name='pregunta seleccion multiple '),
    path('marca', MarcaApi.as_view(), name='marca'),
    path('ultimo_intento', intentos_max),
    path('pregunta_f_v/<int:marca>/',
         PreguntaFoVView.as_view(), name='preguntasFoV'),
    path('pregunta_f_v/create', PreguntaFoVView.as_view(), name='preguntasFoV'),
    path('pausas/<int:marca>/', GetPausesView.as_view(), name="get pauses"),
    path('pregunta_abierta', GetPreguntaAbierta.as_view(), name="pregunta abierta"),
]

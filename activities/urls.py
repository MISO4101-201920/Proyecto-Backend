from activities.views import *
from django.urls import path
from activities.views import CalificarAPI, MarcaApi, intentos_max
app_name = 'activities'


app_name = 'marca'
# add url path to the API
urlpatterns = [
    path('marca', MarcaView.as_view(), name='marca'),
    path('actividad', ActividadView.as_view(), name='actividad'),
    path('resp_estudiante_op_multiple', RespEstudianteMultipleView.as_view(), name='respuesta_estd_op_multiple'),
    path('reports/', reports, name='reports'),
    path('respuestaOpcionMultiple/', RespuestaSeleccionMultipleView.as_view()),
    path('preguntaOpcionMultiple/<int:marca>/', DetailPreguntaSeleccionMultiple.as_view()),
    path('calificacion', CalificarAPI.as_view(), name='calificacion'),
    path('marca', MarcaApi.as_view(), name='marca'),
    path('ultimo_intento', intentos_max)
]
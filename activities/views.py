from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from activities.serializers import MarcaSerializer, ActividadSerializer, RespuestaMultipleEstudianteSerializer, \
    PreguntaOpcionMultipleSerializer
from interactive_content.models import ContenidoInteractivo
from users.models import Profesor
from django.http import HttpResponseNotFound


from .models import Marca, Actividad, RespuestmultipleEstudiante, RespuestaVoF, Opcionmultiple, PreguntaOpcionMultiple


# Create your views here.
@csrf_exempt
def reports(request):

    #Get correct professor through token or session
    try:
        get_the_professor = Profesor.objects.get(id=request.user.id)
    except:
        return HttpResponseNotFound()

    big_json = {}
    big_json['username'] = get_the_professor.username
    big_json['first_name'] = get_the_professor.first_name
    big_json['last_name'] = get_the_professor.last_name
    big_json['email'] = get_the_professor.email
    big_json['direccion'] = get_the_professor.direccion
    big_json['telefono'] = get_the_professor.telefono
    big_json['facultad'] = get_the_professor.facultad
    big_json['marcas'] = []

    marcas = Marca.objects.filter(contenido__contenido__profesor=get_the_professor)
    for marca in marcas:

        big_json['marcas'].append({'nombre':marca.nombre,'actividades':[]})
        actividades = Actividad.objects.filter(marca=marca)

        for actividad in actividades:
            big_json['marcas'][-1]['actividades'].append({'nombre':actividad.nombre, 'preguntas':[]})
    return JsonResponse(big_json)


class MarcaView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # Add permissions to the view
    # permission_classes = [IsAuthenticated]

    # queryset usado para retornar los objetos requeridos
    def get_queryset(self):
        # Add filter to get all the activities of a desired Marca
        contenido = self.request.query_params.get('contenido', None)
        return Marca.objects.filter(contenido=contenido)

    # clase serializer para la transformacion de datos del request
    serializer_class = MarcaSerializer

    def perform_create(self, serializer):
        contenido = get_object_or_404(
            ContenidoInteractivo, id=self.request.data.get('contenido'))
        return serializer.save(contenido=contenido)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ActividadView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # Add permissions to the view
    # permission_classes = [IsAuthenticated]

    # queryset usado para retornar los objetos requeridos
    def get_queryset(self):
        # Add filter to get all the activities of a desired Marca
        marca = self.request.query_params.get('marca', None)
        return Actividad.objects.filter(marca=marca)

    # clase serializer para la transformacion de datos del request
    serializer_class = ActividadSerializer

    def perform_create(self, serializer):
        marca = get_object_or_404(
            Marca, id=self.request.data.get('marca'))
        return serializer.save(marca=marca)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RespEstudianteMultipleView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # Add permissions to the view
    # permission_classes = [IsAuthenticated]

    # Add filter fields for the API
    filterset_fields = ("estudiante", "respuestmultiple")

    # queryset usado para retornar los objetos requeridos
    def get_queryset(self):
        # Add filter to get all the answers of a desired student
        estudiante = self.request.query_params.get('estudiante', None)
        return RespuestmultipleEstudiante.objects.filter(estudiante=estudiante)

    # clase serializer para la transformacion de datos del request
    serializer_class = RespuestaMultipleEstudianteSerializer

    def perform_create(self, serializer):
        pregunta = get_object_or_404(
            Opcionmultiple, id=self.request.data.get('preguntaSeleccionMultiple'))
        return serializer.save(preguntaSeleccionMultiple=pregunta)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CreatePreguntaSeleccionMultiple(APIView):
    def post(self, request, *args, **kwargs):
        question_data = request.data
        marca_id = question_data.pop('marca_id', None)
        if not marca_id:
            interactive_content = ContenidoInteractivo.objects.get(id=question_data['marca'].pop('contenido_id'))
            marca = Marca.objects.create(contenido=interactive_content, **question_data.pop('marca'))
        else:
            marca = Marca.objects.get(pk=marca_id)
        options = question_data.pop('opciones')
        question = PreguntaOpcionMultiple.objects.create(marca=marca, **question_data)
        for option in options:
            Opcionmultiple.objects.create(preguntaSeleccionMultiple=question, **option)
        return Response(data=PreguntaOpcionMultipleSerializer(question).data)

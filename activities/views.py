from rest_framework import status, generics, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from users.models import Profesor
from interactive_content.models import ContenidoInteractivo
from activities.serializers import PreguntaOpcionMultipleSerializer, CalificacionSerializer, RespuestaSeleccionMultipleSerializer, MarcaSerializer
from activities.models import Calificacion,  Marca, Actividad, RespuestmultipleEstudiante,\
    Opcionmultiple, PreguntaOpcionMultiple, PreguntaFoV, RespuestaVoF, Respuesta

# Create your views here.
@api_view(['GET'])
#@authentication_classes([TokenAuthentication])
#@permission_classes([IsAuthenticated])
def reports(request, contentpk):

    #Get correct professor through token or session
    try:
        #get_the_professor = Profesor.objects.get(id=request.user.id)
        get_the_professor = Profesor.objects.get(id=2)
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

        big_json['marcas'].append({'nombre':marca.nombre,'preguntas':[]})
        preguntas_multiples = PreguntaOpcionMultiple.objects.filter(marca=marca)
        preguntas_vof = PreguntaFoV.objects.filter(marca=marca)
        
        for pregunta in preguntas_multiples:
            if isinstance(pregunta, PreguntaOpcionMultiple):
                big_json['marcas'][-1]['preguntas'].append({'pregunta':pregunta.enunciado, 'tipo':'multiple', 'total_respuestas':0,'opciones':[]})
                opciones = Opcionmultiple.objects.filter(preguntaSeleccionMultiple=pregunta)
                
                cont = 0
                for opcion in opciones:
                    votos = RespuestmultipleEstudiante.objects.filter(respuestmultiple=opcion).count()
                    cont+=votos
                    big_json['marcas'][-1]['preguntas'][-1]['opciones'].append({'respuesta':opcion.opcion, 'esCorrecta': opcion.esCorrecta, 'votos':votos})
                big_json['marcas'][-1]['preguntas'][-1]['total_respuestas'] = cont

        for pregunta in preguntas_vof:
            if isinstance(pregunta, PreguntaFoV):
                big_json['marcas'][-1]['preguntas'].append({'pregunta':pregunta.pregunta, 'esCorrecta':pregunta.esVerdadero, 'tipo':'verdadero/falso', 'total_verdadero':0, 'total_falso':0, 'total_respuestas':0})
                howManyTrue = RespuestaVoF.objects.filter(preguntaVoF=pregunta, esVerdadero=True).count() #"howTrue":value
                howManyFalse = RespuestaVoF.objects.filter(preguntaVoF=pregunta, esVerdadero=False).count() #"howFalse":value
                total_vf = howManyTrue + howManyFalse
                big_json['marcas'][-1]['preguntas'][-1]['total_verdadero'] = howManyTrue
                big_json['marcas'][-1]['preguntas'][-1]['total_falso'] = howManyFalse
                big_json['marcas'][-1]['preguntas'][-1]['total_respuestas'] = total_vf

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


class DetailPreguntaSeleccionMultiple(generics.RetrieveUpdateDestroyAPIView, ListModelMixin):
    serializer_class = PreguntaOpcionMultipleSerializer
    lookup_url_kwarg = "marca"

    def get_queryset(self):
        marca = self.kwargs.get(self.lookup_url_kwarg)
        return PreguntaOpcionMultiple.objects.filter(marca=marca)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)


class PreguntaView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # Add permissions to the view
    # permission_classes = [IsAuthenticated]

    # Add filter fields for the API
    filterset_fields = ("actividad",)
    # clase serializer para la transformacion de datos del request
    serializer_class = PreguntaOpcionMultipleSerializer

    # def get_queryset(self):
    # actividad = self.request.query_params.get('actividad')
    # return PreguntaOpcionMultiple.objects.filter(actividad=actividad)

    def perform_create(self, serializer):
        # actividad = get_object_or_404(
        #    Actividad, id=self.request.data.get('actividad'))
        return serializer.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RespuestaSeleccionMultipleView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = RespuestmultipleEstudiante.objects.all()
    # clase serializer para la transformacion de datos del request
    serializer_class = RespuestaSeleccionMultipleSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
         # Validacion de respuesta en blanco (null)
        if self.request.data['respuestmultiple']:
            opcion = Opcionmultiple.objects.filter(
                id=self.request.data['respuestmultiple'])
            pregunta = opcion[0].preguntaSeleccionMultiple
            # valida si el intento de la respuesta es menor o igual al max de intentos permitidos
            if int(self.request.data['intento']) <= pregunta.numeroDeIntentos:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                msj = {'max_attemps': 'Número de intentos maximos excedido'}
                return Response(msj, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CalificarAPI(ListCreateAPIView):
    # Add filter fields for the API
    filterset_fields = ("estudiante", "actividad")
    # serializer usado para la transformacion de datos
    serializer_class = CalificacionSerializer

    # queryset para retornar las calificaciones de un estudiante
    def get_queryset(self):
        student = self.request.query_params.get('estudiante', None)
        activity = self.request.query_params.get('actividad', None)
        if (student):
            return Calificacion.objects.filter(estudiante=student)
        elif (activity):
            return Calificacion.objects.filter(actividad=activity)
        else:
            return Calificacion.objects.filter(actividad=None)
        
        
            


class MarcaApi(ListModelMixin, GenericAPIView):
    serializer_class = MarcaSerializer

    def get_queryset(self):
        content = self.request.query_params.get('contenido', None)
        return Marca.objects.filter(contenido=content)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)


def intentos_max(request):
    if request.method == 'GET':
        pregunta = request.GET.get('id_pregunta')        
        estudiante = request.GET.get('id_estudiante')        
        opciones = Opcionmultiple.objects.filter(
            preguntaSeleccionMultiple=pregunta)

        respuestas = RespuestmultipleEstudiante.objects.filter(
            estudiante=estudiante)
        resps = []

        for respuesta in respuestas:
            for opcion in opciones:
                if respuesta.respuestmultiple == opcion:
                    print('ALGO')
                    if respuesta.intento:
                        resps.append(respuesta.intento)
        if len(resps) > 0:
            max_int = max(resps)
        else: max_int = 0

        print(max_int)
        return JsonResponse({'ultimo_intento': max_int}, status=status.HTTP_200_OK)
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.shortcuts import get_object_or_404

from activities.serializers import MarcaSerializer
from activities.models import Marca
from interactive_content.models import ContenidoInteractivo

# Create your views here.

class MarcaView(ListModelMixin, CreateModelMixin, GenericAPIView):
    # queryset usado para retornar los objetos requeridos
    queryset = Marca.objects.all()
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

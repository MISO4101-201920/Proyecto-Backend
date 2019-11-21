from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from activities.serializers import MarcaSerializer
from interactive_content.models import Contenido, Curso, ContenidoInteractivo


class ContenidoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField()
    url = serializers.URLField()

    class Meta:
        model = Contenido
        fields = ('id', 'nombre', 'url')


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class ContenidoInteractivoSerializer(serializers.ModelSerializer):
    cursos = SerializerMethodField('get_serialized_classes')
    contenido = ContenidoSerializer(read_only=True)
    marcas = MarcaSerializer(read_only=True, many=True)


    class Meta:
        model = ContenidoInteractivo
        fields = '__all__'

    def get_serialized_classes(self, obj):
        return CursoSerializer(obj.curso.all(),many=True).data
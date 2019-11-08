from rest_framework import serializers
from activities.models import Marca, Actividad, RespuestmultipleEstudiante, Opcionmultiple


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ('id', 'nombre', 'punto')

    def create(self, validated_data):
        return Marca.objects.create(**validated_data)


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ('id', 'nombre', 'numeroDeIntentos', 'tieneRetroalimentacion', 'marca')

    def create(self, validated_data):
        return Actividad.objects.create(**validated_data)


class RespuestaMultipleEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestmultipleEstudiante
        fields = ('id', 'seleccionada', 'estudiante', 'respuestmultiple')

    def create(self, validated_data):
        return RespuestmultipleEstudiante.objects.create(**validated_data)


class OpcionmultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcionmultiple
        fields = '__all__'


class PreguntaOpcionMultipleSerializer(serializers.ModelSerializer):
    opcionmultiple_set = OpcionmultipleSerializer(read_only=True, many=True)

    class Meta:
        model = RespuestmultipleEstudiante
        fields = '__all__'

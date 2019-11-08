from rest_framework import serializers

from activities.models import PreguntaOpcionMultiple, RespuestmultipleEstudiante, Opcionmultiple, Calificacion, Marca


class RespuestaSeleccionMultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestmultipleEstudiante
        fields = '__all__'
      

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ('id', 'estudiante', 'actividad', 'calificacion')


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'


class OpcionmultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcionmultiple
        fields = '__all__'


class PreguntaOpcionMultipleSerializer(serializers.ModelSerializer):
    opcionmultiple_set = OpcionmultipleSerializer(read_only=True, many=True)

    class Meta:
        model = RespuestmultipleEstudiante
        fields = '__all__'

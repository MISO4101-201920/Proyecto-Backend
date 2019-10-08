from rest_framework import serializers
from interactive_content.models import Curso


class CursoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Curso
        fields = '__all__'

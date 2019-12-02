import json
from rest_framework.test import APIClient
from django.test import TestCase
from .models import ContenidoInteractivo, Curso
from datetime import datetime

from interactive_content.models import Contenido
from users.models import Profesor, Estudiante
from rest_framework.authtoken.models import Token
from activities.models import Marca


# Create your tests here.
# Create your tests here.
class CreateInteractiveContentTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = Profesor.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

    def test_add_interactive_content(self):
        url = '/content/cont_interactivo'
        self.client.force_login(user=self.user)
        contenido = Contenido.objects.create(url="test.com", nombre="contenido test", profesor_id=self.user.id)
        interactive_content = {"nombre": "test", "contenido": contenido.id}
        response = self.client.post(url, interactive_content, format='json',
                                    HTTP_AUTHORIZATION='Token ' + self.token.key)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['nombre'], 'test')
        self.assertEqual(current_data['contenido']['id'], contenido.id)

    def test_unauthorized_user(self):
        url = '/content/cont_interactivo'
        estudiante = Estudiante.objects.create_user('estudiante', 'estudiante@admin.com', 'estudiante123')
        interactive_content = {"nombre": "test", "contenido": "1"}
        self.token = Token.objects.create(user=estudiante)
        self.client.force_login(user=estudiante)
        Contenido.objects.create(url="test.com", nombre="contenido test", profesor_id=self.user.id)
        response = self.client.post(url, interactive_content, format='json',
                                    HTTP_AUTHORIZATION='Token ' + self.token.key)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['message'], 'Unauthorized')
        self.assertEqual(response.status_code, 401)


class InteractiveContentTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = Profesor.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.url = '/content/interactivecontent/{}'
        self.headers = {'Content-Type': 'application/json'}

    def test_add_interactive_content(self):
        url = '/content/cont_interactivo'
        self.client.force_login(user=self.user)
        contenido = Contenido.objects.create(url="test.com", nombre="contenido test", profesor_id=self.user.id)
        interactive_content = {"nombre": "test", "contenido": contenido.id}
        response = self.client.post(url, interactive_content, format='json',
                                    HTTP_AUTHORIZATION='Token ' + self.token.key)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['nombre'], 'test')
        self.assertEqual(current_data['contenido']['id'], contenido.id)

    def test_unauthorized_user(self):
        url = '/content/cont_interactivo'
        estudiante = Estudiante.objects.create_user('estudiante', 'estudiante@admin.com', 'estudiante123')
        interactive_content = {"nombre": "test", "contenido": "1"}
        self.token = Token.objects.create(user=estudiante)
        self.client.force_login(user=estudiante)
        Contenido.objects.create(url="test.com", nombre="contenido test", profesor_id=self.user.id)
        response = self.client.post(url, interactive_content, format='json',
                                    HTTP_AUTHORIZATION='Token ' + self.token.key)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['message'], 'Unauthorized')
        self.assertEqual(response.status_code, 401)

    def test_get_interactive_content_200_status(self):
        content = Contenido.objects.create(url="youtube.com", nombre="Mi primer contenido", profesor=self.user)
        interactive_content = ContenidoInteractivo.objects.create(contenido=content, fecha_creacion=datetime.now(),
                                                                  tiene_retroalimentacion=True,
                                                                  nombre="Mi primer contenido")
        response = self.client.get(self.url.format(interactive_content.id), format='json', headers=self.headers,
                                   HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_get_interactive_content_info(self):
        content = Contenido.objects.create(url="youtube.com", nombre="Mi primer contenido", profesor=self.user)
        interactive_content = ContenidoInteractivo.objects.create(contenido=content, fecha_creacion=datetime.now(),
                                                                  tiene_retroalimentacion=True,
                                                                  nombre="Mi primer contenido")
        response = self.client.get(self.url.format(interactive_content.id), format='json', headers=self.headers,
                                   HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = json.loads(response.content)

        self.assertEqual(data['nombre'], interactive_content.nombre)
        self.assertEqual(data['tiene_retroalimentacion'], interactive_content.tiene_retroalimentacion)
        self.assertEqual(data['contenido']['nombre'], content.nombre)
        self.assertEqual(data['contenido']['url'], content.url)

    def test_get_courses_from_interactive_content(self):
        content = Contenido.objects.create(url="youtube.com", nombre="Mi primer contenido", profesor=self.user)
        interactive_content = ContenidoInteractivo.objects.create(contenido=content, fecha_creacion=datetime.now(),
                                                                  tiene_retroalimentacion=True)

        curso1 = Curso.objects.create(fecha_creacion=datetime.now(), nombre="Mi primer curso", profesor=self.user,
                                      descripcion="Breve descripcion 1")
        curso2 = Curso.objects.create(fecha_creacion=datetime.now(), nombre="Mi segundo curso", profesor=self.user,
                                      descripcion="Breve descripcion 2")

        interactive_content = ContenidoInteractivo.objects.create(contenido=content, fecha_creacion=datetime.now(),
                                                                  tiene_retroalimentacion=True)
        interactive_content.curso.add(curso1)
        interactive_content.curso.add(curso2)

        response = self.client.get(self.url.format(interactive_content.id), format='json', headers=self.headers,
                                   HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = json.loads(response.content)

        self.assertEqual(data['cursos'][0]['nombre'], interactive_content.curso.first().nombre)
        self.assertEqual(data['cursos'][1]['nombre'], interactive_content.curso.last().nombre)
        self.assertEqual(data['cursos'][0]['descripcion'], interactive_content.curso.first().descripcion)
        self.assertEqual(data['cursos'][1]['descripcion'], interactive_content.curso.last().descripcion)

    def test_get_marcas_from_interactive_content(self):
        content = Contenido.objects.create(url="youtube.com", nombre="Mi primer contenido", profesor=self.user)
        interactive_content = ContenidoInteractivo.objects.create(contenido=content, fecha_creacion=datetime.now(),
                                                                  tiene_retroalimentacion=True)

        marca1 = Marca.objects.create(nombre="Marca 1", punto=100, contenido=interactive_content)
        marca2 = Marca.objects.create(nombre="Marca 2", punto=200, contenido=interactive_content)

        response = self.client.get(self.url.format(interactive_content.id), format='json', headers=self.headers,
                                   HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = json.loads(response.content)

        self.assertEqual(data['marcas'][0]['id'], marca1.id)
        self.assertEqual(data['marcas'][0]['punto'], marca1.punto)
        self.assertEqual(data['marcas'][1]['id'], marca2.id)
        self.assertEqual(data['marcas'][1]['punto'], marca2.punto)


class CourseDetailTestCase(TestCase):

    url = '/content/courses/details/'

    def setUp(self):
        self.client = APIClient()
        self.user = Profesor.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

    def test_get_course_detail(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user(self):
        estudiante = Estudiante.objects.create_user('estudiante', 'estudiante@admin.com', 'estudiante123')
        self.token = Token.objects.create(user=estudiante)
        self.client.force_login(user=estudiante)
        response = self.client.get(self.url, HTTP_AUTHORIZATION='Token ' + self.token.key)
        current_data = json.loads(response.content)
        self.assertEqual(current_data['detail'], 'You do not have permission to perform this action.')
        self.assertEqual(response.status_code, 403)



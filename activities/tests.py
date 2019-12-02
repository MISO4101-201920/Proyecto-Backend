from django.test import TestCase
from django.utils.timezone import make_aware
from datetime import datetime
import json
from django.http import JsonResponse
from rest_framework.utils import json
from django.contrib.auth.models import User, AbstractUser

from interactive_content.models import ContenidoInteractivo, Contenido, Curso, Grupo
from activities.models import Marca, PreguntaOpcionMultiple, Opcionmultiple, Calificacion, RespuestmultipleEstudiante, PreguntaAbierta, RespuestaAbiertaEstudiante, PreguntaFoV, RespuestaVoF
from users.models import Profesor, Estudiante


# Create your tests here.

def escenario():
    naive_datetime = datetime.now()
    aware_datetime = make_aware(naive_datetime)

    profesor = Profesor(facultad="derecho",
                        direccion="cra 76#89-10",
                        telefono="1233322",
                        fecha_creacion=aware_datetime,
                        fecha_modificacion=datetime.now(),
                        username="Pablo123674",
                        email="pablo44@gmail.com",
                        password="qwer44tyu"
                        )
    profesor.id = 33333

    profesor.save()

    estudiante = Estudiante(codigo_de_estudiante="232223555",
                            direccion="cra 76#89-13",
                            telefono="1233323442",
                            fecha_creacion=aware_datetime,
                            fecha_modificacion=datetime.now(),
                            username="Andres1236222r",
                            email="andres222225@gmail.com",
                            password="qwer2222tyu"
                            )

    estudiante.id = 22333

    estudiante.save()

    contenido = Contenido(url="https://www.youtube.com/watch?v=FRivqBxbHRs",
                          nombre="video",
                          profesor=profesor
                          )
    contenido.save()

    curso = Curso(nombre="comunicacion Oral",
                  descripcion="Desarrollar habilidades orales",
                  profesor=profesor
                  )
    curso.save()

    contenidoInteractivo = ContenidoInteractivo(contenido=contenido,
                                                tiene_retroalimentacion=True,
                                                tiempo_disponibilidad=aware_datetime
                                                )
    contenidoInteractivo.save()
    contenidoInteractivo.curso.add(curso)

    marca = Marca(nombre="marca1",
                  punto=33,
                  contenido=contenidoInteractivo
                  )
    marca.save()
    return marca


def escenario2():

    escenario()
    marca = escenario()

    pregunta = PreguntaOpcionMultiple()
    pregunta.nombre = "pregunta1"
    pregunta.enunciado = "enunciado"
    pregunta.numeroDeIntentos = 1
    pregunta.tieneRetroalimentacion = True
    pregunta.esMultipleResp = True
    pregunta.marca_id = marca.id
    pregunta.save()

    opcion = Opcionmultiple(opcion="opcion12",
                            esCorrecta=True,
                            preguntaSeleccionMultiple=pregunta)

    opcion.save()

    return opcion


class PreguntaTestCase(TestCase):

    def test_Get_Pregunta(self):

        marca = escenario()

        pregunta = PreguntaOpcionMultiple()
        pregunta.nombre = "pregunta1"
        pregunta.enunciado = "enunciado"
        pregunta.numeroDeIntentos = 1
        pregunta.tieneRetroalimentacion = True
        pregunta.esMultipleResp = True
        pregunta.marca_id = marca.id
        pregunta.save()

        url = "/activities/preguntaOpcionMultiple" + '/'+str(pregunta.pk)+'/'
        response = self.client.get(url, format='json')
        print(response.context)
        self.assertEqual(response.status_code, 200)

class RespuestaPreguntaAbiertaTestCase(TestCase):

    def test_Guardar_Respuesta(self):

        marca = escenario()
        pregunta = PreguntaAbierta()
        pregunta.nombre = "pregunta1"
        pregunta.numeroDeIntentos = 1
        pregunta.tieneRetroalimentacion = True
        pregunta.marca_id = marca.id
        pregunta.enunciado = "enunciado"
        pregunta.save()

        estudiante = Estudiante.objects.get(username="Andres1236222r")

        curso = Curso.objects.filter(nombre="comunicacion Oral")[0]
        grupo = Grupo(estudiante_id=estudiante.id,
                      curso=curso)
        grupo.save()



        url = "/activities/respuestaAbierta/"

        response = self.client.post(url, {"preguntaAbierta": pregunta.id,
                                          "fecha_creacion": "2019-10-25 23:21:51.950232",
                                          "estudiante": estudiante.pk,
                                          "intento": 1,
                                          "grupo": grupo.id,
                                          "respuesta":"respuesta",
                                          "retroalimentacion" : "retroalimentacion"

                                          }
                                    )

        print(response.context)
        print(response.content)
        self.assertEqual(response.status_code, 201)

class RespuestaPreguntaFoV(TestCase):

    def test_Guardar_Respuesta(self):

        marca = escenario()
        pregunta = PreguntaFoV()
        pregunta.nombre = "pregunta1"
        pregunta.numeroDeIntentos = 1
        pregunta.tieneRetroalimentacion = True
        pregunta.marca_id = marca.id
        pregunta.esVerdadero = True
        pregunta.pregunta = "preguntaPrueba"
        pregunta.save()

        
        estudiante = Estudiante.objects.get(username="Andres1236222r")

        curso = Curso.objects.filter(nombre="comunicacion Oral")[0]
        grupo = Grupo(estudiante_id=estudiante.id,
                      curso=curso)
        grupo.save()

        url = "/activities/respuestafov/"

        response = self.client.post(url, {"preguntaVoF": pregunta.id,
                                          "fecha_creacion": "2019-10-25 23:21:51.950232",
                                          "estudiante": estudiante.pk,
                                          "intento": 1,
                                          "grupo": grupo.id,
                                          "esVerdadero" : True

                                          }
                                    )

        print(response.context)
        print(response.content)
        self.assertEqual(response.status_code, 201)

class RespuestaSeleccionTestCase(TestCase):
    def test_guardar_Respuesta(self):
        opcion = escenario2()
        estudiante = Estudiante.objects.get(username="Andres1236222r")

        curso = Curso.objects.filter(nombre="comunicacion Oral")[0]
        grupo = Grupo(estudiante_id=estudiante.id,
                      curso=curso)
        grupo.save()
        url = "/activities/respuestaOpcionMultiple/"

        response = self.client.post(url, {"respuestmultiple": opcion.id,
                                          "fecha_creacion": "2019-10-25 23:21:51.950232",
                                          "estudiante": estudiante.pk,
                                          "intento": 1,
                                          "curso": grupo.id

                                          }
                                    )

        print(response.context)
        print(response.content)
        self.assertEqual(response.status_code, 201)

    def test_respuesta_vacia(self):
        opcion = escenario2()
        estudiante = Estudiante.objects.get(username="Andres1236222r")

        curso = Curso.objects.filter(nombre="comunicacion Oral")[0]
        grupo = Grupo(estudiante_id=estudiante.id,
                      curso=curso)
        grupo.save()
        url = "/activities/respuestaOpcionMultiple/"

        response = self.client.post(url, {"respuestmultiple": '',
                                          "fecha_creacion": "2019-10-25 23:21:51.950232",
                                          "estudiante": estudiante.pk,
                                          "intento": 1,
                                          "curso": grupo.id
                                          }
                                    )
        
        print(response.context)
        print(response.content)
        self.assertEqual(response.status_code, 201)


class CalificacionCase(TestCase):
    def test_list_calificacion(self):
        url = '/activities/calificacion'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_count_calificaiones(self):
        profe = Profesor.objects.create(
            username='profe12', password='profe123', facultad='Ingenieria')
        contenido = Contenido.objects.create(
            url='www.ejemplo.com', nombre='Contenido', profesor=profe)
        cont_interac = ContenidoInteractivo.objects.create(
            contenido=contenido, tiene_retroalimentacion=False)
        marca = Marca.objects.create(
            nombre='marca', punto=7, contenido=cont_interac)
        pregunta = PreguntaOpcionMultiple.objects.create(
            enunciado='Pregunta 1', esMultipleResp=False, nombre='Actividad 1', numeroDeIntentos=3, tieneRetroalimentacion=True, marca=marca)
        opcion1 = Opcionmultiple.objects.create(
            opcion='A. Opcion1', esCorrecta=True, preguntaSeleccionMultiple=pregunta)
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiant2', password='estudiante123')
        calificacion1 = Calificacion.objects.create(
            estudiante=estudiante1, actividad=pregunta, calificacion=4.5)
        calificacion2 = Calificacion.objects.create(
            estudiante=estudiante2, actividad=pregunta, calificacion=3.5)

        # url = '/activities/calificacion'
        # response = self.client.get(url, format='json')
        # current_data = json.loads(response.content)
        # self.assertEqual(len(current_data), 2)

    def test_filter_calificaiones_by_student(self):
        profe = Profesor.objects.create(
            username='profe12', password='profe123', facultad='Ingenieria')
        contenido = Contenido.objects.create(
            url='www.ejemplo.com', nombre='Contenido', profesor=profe)
        cont_interac = ContenidoInteractivo.objects.create(
            contenido=contenido, tiene_retroalimentacion=False)
        marca = Marca.objects.create(
            nombre='marca', punto=7, contenido=cont_interac)
        pregunta = PreguntaOpcionMultiple.objects.create(
            enunciado='Pregunta 1', esMultipleResp=False, nombre='Actividad 1', numeroDeIntentos=3, tieneRetroalimentacion=True, marca=marca)
        opcion1 = Opcionmultiple.objects.create(
            opcion='A. Opcion1', esCorrecta=True, preguntaSeleccionMultiple=pregunta)
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiant2', password='estudiante123')
        calificacion1 = Calificacion.objects.create(
            estudiante=estudiante1, actividad=pregunta, calificacion=4.5)
        calificacion2 = Calificacion.objects.create(
            estudiante=estudiante2, actividad=pregunta, calificacion=3.5)

        url = '/activities/calificacion?estudiante=1'
        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data), estudiante1.calificacion_set.all().count())

    def test_filter_calificaiones_by_question(self):
        profe = Profesor.objects.create(
            username='profe12', password='profe123', facultad='Ingenieria')
        contenido = Contenido.objects.create(
            url='www.ejemplo.com', nombre='Contenido', profesor=profe)
        cont_interac = ContenidoInteractivo.objects.create(
            contenido=contenido, tiene_retroalimentacion=False)
        marca = Marca.objects.create(
            nombre='marca', punto=7, contenido=cont_interac)
        pregunta = PreguntaOpcionMultiple.objects.create(
            enunciado='Pregunta 1', esMultipleResp=False, nombre='Actividad 1', numeroDeIntentos=3, tieneRetroalimentacion=True, marca=marca)
        pregunta2 = PreguntaOpcionMultiple.objects.create(
            enunciado='Pregunta 2', esMultipleResp=False, nombre='Actividad 2', numeroDeIntentos=1, tieneRetroalimentacion=True, marca=marca)
        opcion1 = Opcionmultiple.objects.create(
            opcion='A. Opcion1', esCorrecta=True, preguntaSeleccionMultiple=pregunta)
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiante2', password='estudiante123')
        calificacion1 = Calificacion.objects.create(
            estudiante=estudiante1, actividad=pregunta, calificacion=4.5)
        calificacion2 = Calificacion.objects.create(
            estudiante=estudiante2, actividad=pregunta, calificacion=3.5)
        calificacion3 = Calificacion.objects.create(
            estudiante=estudiante1, actividad=pregunta2, calificacion=5.0)

        url = '/activities/calificacion?actividad={}'.format(pregunta.id)
        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(current_data['count'], pregunta.calificacion_set.all().count())

    def test_filter_obligatory(self):
        profe = Profesor.objects.create(
            username='profe12', password='profe123', facultad='Ingenieria')
        contenido = Contenido.objects.create(
            url='www.ejemplo.com', nombre='Contenido', profesor=profe)
        cont_interac = ContenidoInteractivo.objects.create(
            contenido=contenido, tiene_retroalimentacion=False)
        marca = Marca.objects.create(
            nombre='marca', punto=7, contenido=cont_interac)
        pregunta = PreguntaOpcionMultiple.objects.create(
            enunciado='Pregunta 1', esMultipleResp=False, nombre='Actividad 1', numeroDeIntentos=3, tieneRetroalimentacion=True, marca=marca)
        pregunta2 = PreguntaOpcionMultiple.objects.create(
            enunciado='Pregunta 2', esMultipleResp=False, nombre='Actividad 2', numeroDeIntentos=1, tieneRetroalimentacion=True, marca=marca)
        opcion1 = Opcionmultiple.objects.create(
            opcion='A. Opcion1', esCorrecta=True, preguntaSeleccionMultiple=pregunta)
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiante2', password='estudiante123')
        calificacion1 = Calificacion.objects.create(
            estudiante=estudiante1, actividad=pregunta, calificacion=4.5)
        calificacion2 = Calificacion.objects.create(
            estudiante=estudiante2, actividad=pregunta, calificacion=3.5)
        calificacion3 = Calificacion.objects.create(
            estudiante=estudiante1, actividad=pregunta2, calificacion=5.0)

        url = '/activities/calificacion'
        response = self.client.get(url, format='json')        
        current_data = json.loads(response.content)

        self.assertEqual(len(current_data['results']), 0)

    def test_create_calificacion(self):
        profe = Profesor.objects.create(
            username='profe12', password='profe123', facultad='Ingenieria')
        contenido = Contenido.objects.create(
            url='www.ejemplo.com', nombre='Contenido', profesor=profe)
        cont_interac = ContenidoInteractivo.objects.create(
            contenido=contenido, tiene_retroalimentacion=False)
        marca = Marca.objects.create(
            nombre='marca', punto=7, contenido=cont_interac)
        pregunta = PreguntaOpcionMultiple.objects.create(
            enunciado='Pregunta 1', esMultipleResp=False, nombre='Actividad 1', numeroDeIntentos=3, tieneRetroalimentacion=True, marca=marca)
        opcion1 = Opcionmultiple.objects.create(
            opcion='A. Opcion1', esCorrecta=True, preguntaSeleccionMultiple=pregunta)
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiante2', password='estudiante123')

        url = '/activities/calificacion'
        data = JsonResponse(
            {"estudiante": "1", "actividad": "1", "calificacion": "3.7"})
        self.client.post(url, {"estudiante": estudiante1.pk, "actividad": pregunta.pk, "calificacion": "3.7"})
        data = JsonResponse(
            {"estudiante": "2", "actividad": "1", "calificacion": "3.7"})
        self.client.post(url, {"estudiante": estudiante2.pk, "actividad": pregunta.pk, "calificacion": "3.7"})

        url = '/activities/calificacion?actividad={}'.format(pregunta.pk)
        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)        
        self.assertEqual(current_data['count'], 2)

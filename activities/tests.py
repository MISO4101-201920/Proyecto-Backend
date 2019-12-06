from django.test import TestCase
from django.utils.timezone import make_aware
from datetime import datetime
import json
from django.http import JsonResponse
from rest_framework.utils import json
from django.contrib.auth.models import User, AbstractUser
from rest_framework.authtoken.models import Token

from interactive_content.models import ContenidoInteractivo, Contenido, Curso, Grupo
from activities.models import Marca, PreguntaOpcionMultiple, Opcionmultiple, Calificacion, RespuestmultipleEstudiante, PreguntaFoV, Pausa,\
    PreguntaAbierta, RespuestaAbiertaEstudiante, PreguntaFoV, RespuestaVoF

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


def escenario3():
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
    return marca, profesor, estudiante, contenidoInteractivo


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
                                          "respuesta": "respuesta",
                                          "retroalimentacion": "retroalimentacion"

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
                                          "esVerdadero": True

                                          }
                                    )

        print(response.context)
        print(response.content)
        self.assertEqual(response.status_code, 201)


class PreguntaFoVTestCase(TestCase):

    # def test_create_question(self):
    #    marca, profesor, estudiante, contInterac = escenario3()
    #    token_prof = Token.objects.create(user=profesor)
    #    url = "/activities/pregunta_f_v/create"
    #    print('=+' * 70)
    #    print(marca.pk)
    #    pregunta = {
    #        "nombre": "test",
    #        "numeroDeIntentos": "1",
    #        "tieneRetroalimentacion": False,
    #        "retroalimentacion": "",
    #        "pregunta": "¿Bogotá es la capital de Colombia?",
    #        "esVerdadero": True,
    #        "marca_id": marca.pk
    #    }
    #    response = self.client.post(
    #        url, pregunta, format='json', HTTP_AUTHORIZATION='Token ' + token_prof.key)
    #    self.assertEqual(response.status_code, 201)

    def test_filter_question(self):
        marca, profesor, estudiante, contInteract = escenario3()
        token_student = Token.objects.create(user=estudiante)
        marca2 = escenario()
        pregunta1 = PreguntaFoV(nombre='test', numeroDeIntentos=1, marca=marca,
                                pregunta="¿Es python un lenguaje compilado?", esVerdadero=False)
        pregunta1.save()
        pregunta2 = PreguntaFoV(nombre='test2', numeroDeIntentos=1, marca=marca,
                                pregunta="¿Django es un framework para apps móviles?", esVerdadero=False)
        pregunta2.save()
        pregunta3 = PreguntaFoV(nombre='test2', numeroDeIntentos=1, marca=marca,
                                pregunta="¿Django es un framework para apps móviles?", esVerdadero=False)
        pregunta3.save()
        pregunta4 = PreguntaFoV(nombre='test2', numeroDeIntentos=1, marca=marca2,
                                pregunta="¿Django es un framework para apps móviles?", esVerdadero=False)
        pregunta4.save()

        url = "/activities/pregunta_f_v/" + str(marca.pk) + "/"
        response = self.client.get(
            url, HTTP_AUTHORIZATION='Token ' + token_student.key, formal='json')
        self.assertEqual(response.status_code, 200)


class GetPauseTestCase(TestCase):
    def test_get_pause(self):
        marca = escenario()
        marca2 = escenario()
        pausa1 = Pausa(nombre='prueba', marca=marca,
                       enunciado='Este es el enunciado de la pausa', tiempo=12.0)
        pausa1.save()
        pausa2 = Pausa(nombre='prueba2', marca=marca,
                       enunciado='Este es el enunciado de la pausa', tiempo=7.0)
        pausa2.save()
        pausa3 = Pausa(nombre='prueba3', marca=marca2,
                       enunciado='Este es el enunciado de la pausa', tiempo=5.0)
        pausa3.save()
        url = '/activities/pausas/' + str(marca2.pk) + '/'
        response = self.client.get(url, formal='json')
        print(response.content)
        current_data = json.loads(response.content)

        self.assertEqual(len(current_data), 1)


class GetPreguntaAbiertaTest(TestCase):
    def test_consulta_preg_abierta(self):
        marca = escenario()
        marca2 = escenario()
        pregunta = PreguntaAbierta(
            nombre='Pregunta abierta', marca=marca, enunciado='¿Que es Django?')
        pregunta.save()
        pregunta2 = PreguntaAbierta(
            nombre='Pregunta abierta', marca=marca, enunciado='¿Que es Django?')
        pregunta2.save()
        pregunta3 = PreguntaAbierta(
            nombre='Pregunta abierta', marca=marca2, enunciado='¿Que es Django?')
        pregunta3.save()
        url = '/activities/pregunta_abierta/' + str(marca.pk) + '/'
        response = self.client.get(url, formal='json')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data), 2)


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
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiant2', password='estudiante123')

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
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiant2', password='estudiante123')
        calificacion1 = Calificacion.objects.create(
            estudiante=estudiante1, actividad=pregunta, calificacion=4.5)

        url = '/activities/calificacion?estudiante=1'
        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data),
                         estudiante1.calificacion_set.all().count())

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
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiante2', password='estudiante123')
        calificacion1 = Calificacion.objects.create(
            estudiante=estudiante1, actividad=pregunta, calificacion=4.5)

        url = '/activities/calificacion?actividad={}'.format(pregunta.id)
        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(current_data['count'],
                         pregunta.calificacion_set.all().count())

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
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiante2', password='estudiante123')

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
        estudiante1 = Estudiante.objects.create(
            username='esrudiante', password='estudiante123')
        estudiante2 = Estudiante.objects.create(
            username='esrudiante2', password='estudiante123')

        url = '/activities/calificacion'

        self.client.post(url, {"estudiante": estudiante1.pk,
                               "actividad": pregunta.pk, "calificacion": "3.7"})

        self.client.post(url, {"estudiante": estudiante2.pk,
                               "actividad": pregunta.pk, "calificacion": "3.7"})

        url = '/activities/calificacion?actividad={}'.format(pregunta.pk)
        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(current_data['count'], 2)

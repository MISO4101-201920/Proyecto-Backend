from random import randint

from activities.models import Marca
from interactive_content.models import Contenido, ContenidoInteractivo, Curso
from users.models import Profesor

test_profesor = Profesor.objects.create(username="cr.daza1211@uniandes.edu.co",
                                        password="password", first_name="Carlos",
                                        last_name="Daza", email="cr.daza1211@uniandes.edu.co")
contents = ['https://www.youtube.com/watch?v=nSxq1EgWyKo&list=PL4n8DMiz102FvLpI0FUP6-kFNE0YiwLcv&index=1',
            'https://www.youtube.com/watch?v=nSxq1EgWyKo&list=PL4n8DMiz102FvLpI0FUP6-kFNE0YiwLcv&index=2',
            'https://www.youtube.com/watch?v=nSxq1EgWyKo&list=PL4n8DMiz102FvLpI0FUP6-kFNE0YiwLcv&index=3',
            'https://www.youtube.com/watch?v=nSxq1EgWyKo&list=PL4n8DMiz102FvLpI0FUP6-kFNE0YiwLcv&index=4']
curso1 = Curso.objects.create(nombre="Mi primer curso", profesor=test_profesor, descripcion="Breve descripcion 1")
curso2 = Curso.objects.create(nombre="Mi segundo curso", profesor=test_profesor, descripcion="Breve descripcion 2")
i = 1
for url in contents:
    content = Contenido.objects.create(url=url, nombre="fin de sprint {}".format(i), profesor=test_profesor)
    interactive_content = ContenidoInteractivo.objects.create(contenido=content, tiene_retroalimentacion=True)
    to_course = randint(0, 100)
    if to_course % 2 == 0:
        interactive_content.curso.add(curso1)
    elif to_course % 3 == 0:
        interactive_content.curso.add(curso2)
    Marca.objects.create(nombre="Marca 1", punto=10, contenido=interactive_content)
    Marca.objects.create(nombre="Marca 2", punto=60, contenido=interactive_content)
    i += 1
## Cursos disponibles:

- Linux [15 horas]
- Personalizacion [3 horas]
- Hacking [53]

## Instalacion

Instala el paquete usando `pip3`:

```python3
pip3 install hack4u
```

## Uso basico

### Listar todos los cursos

```python
from hack4u import list_courses

for course in list_courses():
	print(course)
```

### Obtener un curso por nombre

```python
from hack4u import get_course_by_name

course = get_course_by_name("Linux")
print(course
```

### Calcular duracion total de los cursos

```python3
from hack4u.utils import total_duration

print(f"Duracion total: {total_duration()} horas")
```

# Warehouse Management System

Este proyecto es un sistema de gestión de inventarios de productos, que incluye la funcionalidad de CRUD para productos y órdenes, así como validación de stock y manejo de errores.

## Tecnologías utilizadas

- **Python 3.10**
- **Django** (backend)
- **Django REST Framework** (API REST)
- **PostgreSQL** (base de datos)
- **Poetry** (gestión de dependencias)
- **Docker** (contenedorización)
- **pytest** (testing)
- **pytest-django** (integración de testing con Django)

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado lo siguientes recursos:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Instalación

### Clonar el repositorio

```bash
git clone https://github.com/arnblanco/bbb-backend
cd tu_proyecto
```

### Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto con las siguientes variables:

```bash
DJANGO_CONFIGURATION=
SECRET_KEY=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```

### Ejecutar Docker

Construir e iniciar el proyecto

```bash
docker compose up --build -d
```

## Uso

### Ejecutar el servidor

Con los contenedores en ejecución, el servidor Django estará disponible en:
```bash
Api Host: http://localhost:8000/api/
Swagger: http://localhost:8000/swagger/
Redoc: http://localhost:8000/redoc/
```

## Estructura del proyecto

```bash
.
├── _apps
│   ├── warehouse
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── ...
│   ├── tests
│   │   ├── conftest.py
│   │   ├── warehouse
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   ├── test_serializers.py
├── core
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── pyproject.toml
├── poetry.lock
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

### Uso de `django-configurations` para la gestión de configuración

Este proyecto utiliza [`django-configurations`](https://django-configurations.readthedocs.io/en/stable/) para manejar la configuración de Django de manera basada en clases y específica para cada entorno. Este enfoque facilita la separación de configuraciones comunes y específicas para cada entorno, como desarrollo y producción.

#### Cómo funciona `django-configurations`

En este proyecto, el archivo `settings.py` define tres clases principales de configuración:

- **`Common`**:
  - Contiene la configuración base compartida entre todos los entornos.
  - Incluye las aplicaciones instaladas, middleware, configuración de base de datos, configuración de logs, etc.

- **`Dev`**:
  - Extiende la clase `Common` y agrega configuraciones específicas del entorno de desarrollo, como habilitar el modo `DEBUG` y permitir solicitudes CORS desde localhost.

- **`Prod`**:
  - Extiende la clase `Common` y contiene configuraciones específicas para producción, enfocándose en características de seguridad como el uso obligatorio de SSL y deshabilitar el modo `DEBUG`.

## Testing

Este proyecto usa pytest para realizar pruebas. Los archivos de test se encuentran en la carpeta tests/warehouse/, organizados en:
- test_models.py: Pruebas unitarias para los modelos.
- test_views.py: Pruebas unitarias para las vistas.
- test_serializers.py: Pruebas unitarias para los serializers.

## Ejecutar pruebas
Para ejecutar las pruebas, simplemente usa:

```bash
docker-compose exec web poetry run pytest
```
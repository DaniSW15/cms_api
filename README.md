# CMS API

Una API simple para gestionar contenido con usuarios, posts, categorías, comentarios y más.

## Requisitos

- Python 3.8+
- Docker y Docker Compose (opcional)
- PostgreSQL (si no usas Docker)

## Instalación

### 1. Clonar el proyecto
```bash
git clone <url-del-repo>
cd cms_api
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto con las variables necesarias.

### 5. Ejecutar migraciones
```bash
alembic upgrade head
```

## Ejecutar la aplicación

### Opción 1: Localmente
```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

### Opción 2: Con Docker
```bash
docker-compose up
```

## Estructura del proyecto

```
app/
├── api/           # Endpoints y rutas
├── core/          # Configuración y utilidades
├── db/            # Conexión a base de datos
├── models/        # Modelos de base de datos
├── repositories/  # Acceso a datos
├── schemas/       # Esquemas Pydantic
├── services/      # Lógica de negocio
└── utils/         # Funciones auxiliares

alembic/          # Migraciones de base de datos
tests/            # Tests de la aplicación
```

## API Endpoints

- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/users` - Crear usuario
- `GET /api/v1/posts` - Listar posts
- `POST /api/v1/posts` - Crear post
- `GET /api/v1/categories` - Listar categorías
- `GET /api/v1/comments` - Listar comentarios

## Documentación

Una vez la aplicación está corriendo, acceder a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Desarrollo

Para ejecutar los tests:
```bash
pytest
```

## Licencia

MIT

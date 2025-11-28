# ScoutMe - Plataforma de Conexión entre Jugadores y Ojeadores

ScoutMe es una plataforma web que conecta jugadores deportivos con ojeadores profesionales, facilitando el descubrimiento de talento y la organización de eventos deportivos.

## Características Principales

- **Sistema de Roles**: Registro diferenciado para jugadores y ojeadores
- **Perfiles Personalizados**: Perfiles editables con información deportiva detallada
- **Gestión de Videos**: Subida de videos locales o enlaces de YouTube
- **Buscador Avanzado**: Filtros por deporte, posición, edad, ubicación y nivel
- **Eventos Deportivos**: Creación y gestión de eventos por ojeadores
- **Mensajería Interna**: Sistema de mensajes entre usuarios
- **Panel de Administración**: Gestión de usuarios y contenido

## Tecnologías Utilizadas

- **Backend**: Flask 3.0.0
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Autenticación**: Flask-Login 0.6.3
- **Formularios**: Flask-WTF 1.2.1
- **Seguridad**: Flask-Bcrypt 1.0.1
- **Frontend**: Bootstrap 5.3 (CDN)

## Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- virtualenv (recomendado)

## Instalación y Configuración

### 1. Clonar o descargar el proyecto
```bash
cd scoutme
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Copiar el archivo `.env.example` a `.env` y ajustar las variables:
```bash
cp .env.example .env
```

Editar `.env` con tus configuraciones:
```
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DATABASE_URI=sqlite:///scoutme.db
FLASK_ENV=development
```

### 6. Inicializar la base de datos
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Base de datos creada')"
```

### 7. Cargar datos de prueba (opcional pero recomendado)
```bash
python seed.py
```

Esto creará:
- 1 usuario administrador (admin@scoutme.com / admin123)
- 3 ojeadores de prueba
- 6 jugadores de prueba con videos

### 8. Ejecutar la aplicación
```bash
python run.py
```

O alternativamente:
```bash
flask run
```

La aplicación estará disponible en: `http://localhost:5000`

## Usuarios de Prueba

Después de ejecutar `seed.py`:

**Administrador:**
- Email: admin@scoutme.com
- Password: admin123

**Ojeadores:**
- Email: ojeador1@scoutme.com / Password: ojeador123
- Email: ojeador2@scoutme.com / Password: ojeador123
- Email: ojeador3@scoutme.com / Password: ojeador123

**Jugadores:**
- Email: jugador1@scoutme.com / Password: jugador123
- Email: jugador2@scoutme.com / Password: jugador123
- (etc., hasta jugador6)

## Estructura del Proyecto
```
scoutme/
├── app.py                 # Aplicación Flask principal y rutas
├── models.py              # Modelos de base de datos
├── forms.py               # Formularios WTForms
├── config.py              # Configuración de la aplicación
├── requirements.txt       # Dependencias del proyecto
├── run.py                 # Script para ejecutar la aplicación
├── seed.py                # Script para datos de prueba
├── README.md              # Este archivo
├── .env.example           # Plantilla de variables de entorno
├── /static                # Archivos estáticos
│   ├── css/
│   │   └── main.css      # Estilos personalizados
│   └── js/
│       └── main.js       # JavaScript personalizado
├── /templates             # Templates Jinja2
│   ├── base.html         # Template base
│   ├── home.html         # Página de inicio
│   ├── login.html        # Inicio de sesión
│   ├── register_jugador.html
│   ├── register_ojeador.html
│   ├── perfil_jugador.html
│   ├── perfil_ojeador.html
│   ├── buscar.html       # Buscador de jugadores
│   ├── eventos.html      # Lista de eventos
│   ├── evento_detalle.html
│   ├── mensajes.html     # Sistema de mensajería
│   └── admin.html        # Panel de administración
└── /uploads               # Videos subidos (creado automáticamente)
```

## Características de Seguridad

- **Contraseñas hasheadas**: Bcrypt para almacenamiento seguro
- **Protección CSRF**: Tokens en todos los formularios
- **Validación de entrada**: WTForms con validadores
- **Control de acceso**: Decoradores para rutas protegidas
- **Sanitización de archivos**: Validación de tipos y tamaños de video

## Gestión de Videos

- **Formatos soportados**: mp4, mov, webm, mkv
- **Tamaño máximo**: 100 MB por video
- **Almacenamiento**: Local en carpeta `/uploads`
- **YouTube**: Soporte para enlaces directos

## Despliegue a Producción

### Migración a PostgreSQL

1. Instalar psycopg2:
```bash
pip install psycopg2-binary
```

2. Actualizar `DATABASE_URI` en `.env`:
```
DATABASE_URI=postgresql://usuario:password@localhost/scoutme
```

### Configuración con Gunicorn y Nginx

1. Instalar Gunicorn:
```bash
pip install gunicorn
```

2. Ejecutar con Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. Configurar Nginx como proxy inverso:
```nginx
server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /ruta/a/scoutme/static;
    }

    location /uploads {
        alias /ruta/a/scoutme/uploads;
    }
}
```

### Almacenamiento en la Nube (S3)

Para almacenar videos en AWS S3:
1. Instalar boto3: `pip install boto3 flask-s3`
2. Configurar credenciales AWS
3. Modificar funciones de subida en `app.py`

## API de Ejemplo

### Buscar Jugadores por Deporte y Ciudad

**Request:**
```bash
curl -X GET "http://localhost:5000/api/buscar?deporte=fútbol&ciudad=Buenos%20Aires" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "jugadores": [
    {
      "id": 1,
      "nombre": "Lionel Pérez",
      "deporte": "fútbol",
      "posicion": "delantero",
      "edad": 22,
      "pais": "Argentina",
      "ciudad": "Buenos Aires",
      "nivel": "semi-profesional",
      "descripcion": "Delantero rápido con excelente definición"
    },
    {
      "id": 3,
      "nombre": "Diego Martínez",
      "deporte": "fútbol",
      "posicion": "mediocampista",
      "edad": 24,
      "pais": "Argentina",
      "ciudad": "Buenos Aires",
      "nivel": "profesional",
      "descripcion": "Mediocampista creativo con gran visión de juego"
    }
  ],
  "total": 2,
  "pagina": 1,
  "por_pagina": 20
}
```

## Solución de Problemas

### Error al crear la base de datos
```bash
# Eliminar base de datos existente
rm instance/scoutme.db
# Recrear
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Error de permisos en /uploads
```bash
mkdir uploads
chmod 755 uploads
```

### Puerto 5000 ya en uso
```bash
# Ejecutar en otro puerto
flask run --port 5001
```

## Contribuciones

Este es un proyecto base. Contribuciones y mejoras son bienvenidas.

## Licencia

MIT License - Uso libre para proyectos personales y comerciales.

## Soporte

Para reportar problemas o sugerencias, crear un issue en el repositorio del proyecto.
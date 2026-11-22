# BWT5_BusinessWork

Gestión documental con avisos de vencimiento: cada usuario registra sus documentos y la aplicación le muestra cuáles ya vencieron, cuáles están por vencer y cuáles siguen vigentes.

| Ingreso | Documentos del usuario |
|---|---|
| ![Pantalla de ingreso](docs/img/ingreso.png) | ![Panel con el estado de cada documento](docs/img/documentos.png) |

## Desafío

¿Cómo construir una solución tecnológica donde sea posible autenticarse como usuario para descargar y cargar documentos de diversa índole?

Realizar la gestión documental de manera manual genera problemas de inconsistencia de datos, no se obtienen alertas de notificación de documentos a expirar, y se podría incurrir en problemas legales. Por ejemplo: la vigencia de un documento expira y, como no hay alertas, la empresa sigue usando un documento caducado.

## Cómo funciona

```mermaid
flowchart LR
    N["Navegador<br/>(frontend/)"] -->|"POST /login · GET /users/..."| A["FastAPI<br/>(backend/sql_app)"]
    A --> B[("SQLite por defecto<br/>o PostgreSQL")]
```

Una sola aplicación sirve la página y la API, así que se levanta con un comando.

Cada documento tiene una fecha de vencimiento y unos días de aviso (`notificacion`). Con eso la API calcula su estado:

| Estado | Cuándo |
|---|---|
| `vencido` | La fecha de vencimiento ya pasó |
| `por_vencer` | Faltan los días de aviso o menos |
| `vigente` | Falta más que los días de aviso |

### Modelo de datos

```mermaid
erDiagram
    DEPARTAMENTOS ||--o{ USERS : agrupa
    USERS ||--o{ DOCUMENTOS : registra
    DEPARTAMENTOS {
        int id_departamento PK
        string name_dep
    }
    USERS {
        string username PK
        string email
        string name
        string last_name
        bigint celular
        int dep_id_dep FK
        string password "hash PBKDF2"
    }
    DOCUMENTOS {
        int id_documento PK
        string name_document
        date expiracion
        int notificacion "días de aviso"
        string descripcion
        string Users_username FK
    }
```

### Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| `POST` | `/login` | Valida usuario y contraseña |
| `POST` | `/departamentos/` | Crea un departamento |
| `GET` | `/departamentos/` | Lista los departamentos con sus usuarios |
| `POST` | `/users/?dep_id=1` | Crea un usuario en un departamento |
| `GET` | `/users/` | Lista los usuarios |
| `GET` | `/users/{username}` | Consulta un usuario con sus documentos |
| `POST` | `/users/{username}/documents/` | Registra un documento para el usuario |
| `GET` | `/documents/` | Lista todos los documentos |

La documentación interactiva queda en `/docs`.

## Cómo ejecutarlo

Requiere Python 3.11 o superior.

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m backend.sql_app.datos_demo
uvicorn backend.sql_app.main:app --reload
```

Abre <http://127.0.0.1:8000> e ingresa con `demo` / `demo1234`. El segundo comando crea un departamento, ese usuario y tres documentos, uno en cada estado; si se repite no duplica nada.

## Configuración

| Variable | Para qué sirve | Valor por defecto |
|---|---|---|
| `DATABASE_URL` | Base de datos | `sqlite:///./btw5.db` (un archivo local) |

Para PostgreSQL: `export DATABASE_URL="postgresql://usuario:clave@localhost/btw5"`.

## Pruebas

```bash
pip install -r requirements-dev.txt
pytest
```

Son 38 pruebas sobre departamentos, usuarios, documentos, ingreso, la página y los datos de demostración. Usan una base SQLite en memoria.

## Qué hay en el repositorio

| Ruta | Contenido |
|---|---|
| `backend/sql_app/` | API en FastAPI con SQLAlchemy |
| `frontend/` | Página de ingreso y panel de documentos (HTML, CSS y JS) |
| `tests/` | Pruebas automáticas |
| `Arbol_de_Descomposicion_Funconal/` | Árbol de descomposición funcional (draw.io) |
| `DiseñosMockup/` | Diseño preliminar de la interfaz |

## Límites

- El ingreso valida la contraseña pero no crea sesión ni token: los endpoints de la API no están protegidos. Sirve como demostración, no para datos reales.
- Se registran los datos del documento (nombre, vencimiento, aviso), no el archivo: todavía no hay carga ni descarga de archivos.
- Los avisos se ven en la página; no se envían por correo ni por otro canal.
- Las pruebas corren sobre SQLite. Con PostgreSQL no se probó en esta revisión.
- Las tablas se crean si no existen, pero no se migran: una base creada con la versión anterior (celular de 32 bits, claves en texto plano) hay que recrearla.

## Licencia

CC0 1.0 Universal. Ver [LICENSE](LICENSE).

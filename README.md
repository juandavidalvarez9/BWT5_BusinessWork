# BWT5_BusinessWork

> **Estado:** proyecto de 2020, sin mantenimiento. Se conserva como archivo.

Prototipo de gestión documental: autenticación de usuarios para cargar y descargar documentos, con la idea de avisar cuando un documento está por vencer.

## Desafío
¿Cómo construir una solución tecnológica donde sea posible autenticarse como usuario para descargar y cargar documentos de diversa índole?

## Descripción
Realizar la gestión documental de manera manual genera problemas de inconsistencia de datos, no se obtienen alertas de notificación de documentos a expirar, y se podría incurrir en problemas legales.

## Caso explicativo
La vigencia de un documento expira. Como no se tienen alertas y notificaciones en una plataforma debido a una gestión documental manual, la empresa incurre en problemas legales por usar documentos caducados.

## Qué hay en el repositorio

| Ruta | Contenido |
|---|---|
| `BTW5_BusinessWork.html`, `css/`, `js/`, `img/` | Interfaz web (HTML, CSS y JS) |
| `backend/sql_app/` | API en FastAPI con SQLAlchemy sobre PostgreSQL |
| `Arbol_de_Descomposicion_Funconal/` | Árbol de descomposición funcional (draw.io) |
| `DiseñosMockup/` | Diseño preliminar de la interfaz |

## Configuración del backend

La conexión a la base de datos se lee de la variable de entorno `DATABASE_URL`:

```bash
pip install -r requirements.txt
export DATABASE_URL="postgresql://usuario:clave@localhost/btw5"
uvicorn backend.sql_app.main:app --reload
```

## Licencia
CC0 1.0 Universal. Ver [LICENSE](LICENSE).

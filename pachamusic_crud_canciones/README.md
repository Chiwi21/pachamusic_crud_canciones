# CRUD OOP de Canciones - PachaMusicDB

Proyecto para Base de Datos II. El sistema implementa un CRUD orientado a objetos en Python para la tabla `dbo.Cancion` de la base `PachaMusicDB`, usando conexión con `config.json` y procedimientos almacenados en SQL Server.

## Archivos

- `gestor_canciones.py`: programa principal en Python con la clase `GestorCanciones`.
- `config.json`: archivo de configuración de conexión.
- `sp_crud_cancion.sql`: procedimientos almacenados para crear, consultar, actualizar y eliminar canciones.
- `informe_crud_canciones_pachamusic.docx`: informe editable con estructura y espacios para evidencias.

## Requisitos

- Python 3.x
- SQL Server
- ODBC Driver 17 for SQL Server
- Librería `pyodbc`

Instalación de pyodbc:

```bash
pip install pyodbc
```

## Configuración

Editar `config.json` con los datos del servidor local:

```json
{
  "name_server": "LAPTOP-SJ66TR29",
  "database": "PachaMusicDB",
  "username": "pm_app_login",
  "password": "PachaMusic#2026",
  "controlador_odbc": "ODBC Driver 17 for SQL Server",
  "trust_server_certificate": "yes"
}
```

## Ejecución en SQL Server

Ejecutar primero:

```sql
sp_crud_cancion.sql
```

Este script crea los procedimientos:

- `dbo.sp_CRUD_CrearCancion`
- `dbo.sp_CRUD_ConsultarCanciones`
- `dbo.sp_CRUD_ActualizarCancion`
- `dbo.sp_CRUD_EliminarCancion`

## Ejecución en Python

Desde la carpeta del proyecto:

```bash
python gestor_canciones.py
```

## Nota sobre eliminación

La eliminación se implementa de forma segura. Si una canción tiene relaciones con reproducciones, likes, playlists, géneros, ventas o descargas, el procedimiento no la borra físicamente; la marca como `Inactiva`. Si no tiene dependencias, se elimina de la tabla.

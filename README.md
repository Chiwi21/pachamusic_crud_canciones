# PachaMusicDB - Versión Django

Migración del proyecto original en Flask a Django. La interfaz conserva las mismas páginas, rutas principales y llamadas a procedimientos almacenados de SQL Server mediante `pyodbc`.

## Estructura principal

```text
pachamusic_django/
├── manage.py
├── config.json
├── requirements.txt
├── sp_crud_cancion.sql
├── sp_adicionales.sql
├── pachamusic_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/
    ├── db.py
    ├── views.py
    ├── urls.py
    ├── jinja2.py
    ├── context_processors.py
    └── templates/
```

## Requisitos

- Python 3.x
- SQL Server con la base de datos `PachaMusicDB`
- ODBC Driver 17 o 18 para SQL Server
- Procedimientos almacenados instalados en la base de datos
- PowerShell o Terminal de Windows

## Instalación

### 1. Abrir PowerShell en la carpeta del proyecto

Todos los comandos deben ejecutarse desde la carpeta raíz del proyecto.

Puedes hacerlo de cualquiera de estas formas:

- Clic derecho dentro de la carpeta → **Abrir en Terminal**
- Escribir `powershell` en la barra de direcciones del Explorador de Windows y presionar Enter

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Configurar la conexión a la base de datos

Edita el archivo `config.json` con los datos de tu instancia de SQL Server.

Ejemplo:

```json
{
  "name_server": "(localdb)\\Alfredo",
  "database": "PachaMusicDB",
  "username": "pm_app_login",
  "password": "PachaMusic#2026",
  "controlador_odbc": "ODBC Driver 18 for SQL Server",
  "trust_server_certificate": "yes"
}
```

Luego ejecuta los scripts en este orden:

```text
1. loginsql
2. sp_crud_canciones
3. sp_adicionales

```
## Ejecutar el proyecto

Aplicar las migraciones internas de Django:

```powershell
python manage.py migrate
```

Iniciar el servidor:

```powershell
python manage.py runserver
```

Luego abre en tu navegador:

```text
http://127.0.0.1:8000/
```

## Notas de migración

- Django utiliza SQLite únicamente para sesiones y funcionalidades internas del framework.
- La base de datos `PachaMusicDB` no se administra mediante modelos Django.
- La lógica de acceso a datos continúa utilizando procedimientos almacenados y `pyodbc`.
- Las plantillas Jinja originales fueron conservadas mediante el backend Jinja2 de Django.
- Se implementaron funciones de compatibilidad para mantener el comportamiento del proyecto original en Flask.

## Solución de problemas

### Error de conexión a SQL Server

Verifica que:

- SQL Server esté en ejecución.
- Los datos de `config.json` sean correctos.
- El controlador ODBC especificado esté instalado.

### Error: "No module named pyodbc"

Ejecuta nuevamente:

```powershell
pip install -r requirements.txt
```

### Puerto 8000 ocupado

Puedes iniciar el servidor en otro puerto:

```powershell
python manage.py runserver 8080
```

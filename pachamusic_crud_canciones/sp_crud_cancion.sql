/* =========================================================
   CRUD de Canciones para PachaMusicDB
   Objetivo: procedimientos almacenados invocados desde Python
   Tabla: dbo.Cancion
   ========================================================= */

USE PachaMusicDB;
GO

/* =========================================================
   1. Crear canción
   Nota: id_cancion es IDENTITY, por eso no se recibe como parámetro.
   ========================================================= */
CREATE OR ALTER PROCEDURE dbo.sp_CRUD_CrearCancion
    @id_album INT,
    @titulo_cancion VARCHAR(150),
    @duracion_segundos INT,
    @estado_cancion VARCHAR(20),
    @fecha_publicacion DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM dbo.Album WHERE id_album = @id_album)
    BEGIN
        RAISERROR('El album indicado no existe.', 16, 1);
        RETURN;
    END;

    IF @duracion_segundos <= 0
    BEGIN
        RAISERROR('La duracion debe ser mayor que cero.', 16, 1);
        RETURN;
    END;

    IF @estado_cancion NOT IN ('Activa', 'Inactiva')
    BEGIN
        RAISERROR('El estado de la cancion debe ser Activa o Inactiva.', 16, 1);
        RETURN;
    END;

    INSERT INTO dbo.Cancion
    (
        id_album,
        titulo_cancion,
        duracion_segundos,
        estado_cancion,
        fecha_publicacion
    )
    VALUES
    (
        @id_album,
        @titulo_cancion,
        @duracion_segundos,
        @estado_cancion,
        @fecha_publicacion
    );

    SELECT
        SCOPE_IDENTITY() AS id_cancion_generada,
        'Cancion creada correctamente.' AS mensaje;
END;
GO

/* =========================================================
   2. Consultar canciones
   Si @id_cancion es NULL, lista todas las canciones.
   Si @id_cancion tiene valor, consulta solo una canción.
   ========================================================= */
CREATE OR ALTER PROCEDURE dbo.sp_CRUD_ConsultarCanciones
    @id_cancion INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        c.id_cancion,
        c.id_album,
        a.nombre_album,
        ar.nombre_artista,
        c.titulo_cancion,
        c.duracion_segundos,
        c.estado_cancion,
        c.fecha_publicacion,
        c.reproducciones_totales,
        c.likes_totales
    FROM dbo.Cancion c
    INNER JOIN dbo.Album a
        ON c.id_album = a.id_album
    INNER JOIN dbo.Artista ar
        ON a.id_artista = ar.id_artista
    WHERE (@id_cancion IS NULL OR c.id_cancion = @id_cancion)
    ORDER BY c.id_cancion;
END;
GO

/* =========================================================
   3. Actualizar canción
   No actualiza reproducciones_totales ni likes_totales porque esos
   campos son controlados por reglas/triggers del sistema.
   ========================================================= */
CREATE OR ALTER PROCEDURE dbo.sp_CRUD_ActualizarCancion
    @id_cancion INT,
    @id_album INT,
    @titulo_cancion VARCHAR(150),
    @duracion_segundos INT,
    @estado_cancion VARCHAR(20),
    @fecha_publicacion DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM dbo.Cancion WHERE id_cancion = @id_cancion)
    BEGIN
        RAISERROR('La cancion indicada no existe.', 16, 1);
        RETURN;
    END;

    IF NOT EXISTS (SELECT 1 FROM dbo.Album WHERE id_album = @id_album)
    BEGIN
        RAISERROR('El album indicado no existe.', 16, 1);
        RETURN;
    END;

    IF @duracion_segundos <= 0
    BEGIN
        RAISERROR('La duracion debe ser mayor que cero.', 16, 1);
        RETURN;
    END;

    IF @estado_cancion NOT IN ('Activa', 'Inactiva')
    BEGIN
        RAISERROR('El estado de la cancion debe ser Activa o Inactiva.', 16, 1);
        RETURN;
    END;

    UPDATE dbo.Cancion
       SET id_album = @id_album,
           titulo_cancion = @titulo_cancion,
           duracion_segundos = @duracion_segundos,
           estado_cancion = @estado_cancion,
           fecha_publicacion = @fecha_publicacion
     WHERE id_cancion = @id_cancion;

    SELECT
        @id_cancion AS id_cancion_actualizada,
        'Cancion actualizada correctamente.' AS mensaje;
END;
GO

/* =========================================================
   4. Eliminar canción
   Eliminación segura:
   - Si la canción tiene dependencias, se marca como Inactiva.
   - Si no tiene dependencias, se elimina físicamente.
   Esto protege la integridad referencial del Proyecto Integrador.
   ========================================================= */
CREATE OR ALTER PROCEDURE dbo.sp_CRUD_EliminarCancion
    @id_cancion INT
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM dbo.Cancion WHERE id_cancion = @id_cancion)
    BEGIN
        RAISERROR('La cancion indicada no existe.', 16, 1);
        RETURN;
    END;

    IF EXISTS (SELECT 1 FROM dbo.Cancion_Genero WHERE id_cancion = @id_cancion)
       OR EXISTS (SELECT 1 FROM dbo.Playlist_Cancion WHERE id_cancion = @id_cancion)
       OR EXISTS (SELECT 1 FROM dbo.[Like] WHERE id_cancion = @id_cancion)
       OR EXISTS (SELECT 1 FROM dbo.Reproduccion WHERE id_cancion = @id_cancion)
       OR EXISTS (SELECT 1 FROM dbo.Detalle_Venta WHERE id_cancion = @id_cancion)
       OR EXISTS (SELECT 1 FROM dbo.Descarga WHERE id_cancion = @id_cancion)
    BEGIN
        UPDATE dbo.Cancion
           SET estado_cancion = 'Inactiva'
         WHERE id_cancion = @id_cancion;

        SELECT
            @id_cancion AS id_cancion,
            'La cancion tiene dependencias; se realizo eliminacion logica cambiando el estado a Inactiva.' AS mensaje;
        RETURN;
    END;

    DELETE FROM dbo.Cancion
    WHERE id_cancion = @id_cancion;

    SELECT
        @id_cancion AS id_cancion,
        'Cancion eliminada fisicamente correctamente.' AS mensaje;
END;
GO

/* =========================================================
   5. Permisos para ejecución desde Python
   ========================================================= */
GRANT EXECUTE ON dbo.sp_CRUD_CrearCancion TO rol_app_executor;
GRANT EXECUTE ON dbo.sp_CRUD_ConsultarCanciones TO rol_app_executor;
GRANT EXECUTE ON dbo.sp_CRUD_ActualizarCancion TO rol_app_executor;
GRANT EXECUTE ON dbo.sp_CRUD_EliminarCancion TO rol_app_executor;
GO

/* Si se utiliza directamente un usuario SQL distinto, descomentar y adaptar:
GRANT EXECUTE ON dbo.sp_CRUD_CrearCancion TO pm_app_user;
GRANT EXECUTE ON dbo.sp_CRUD_ConsultarCanciones TO pm_app_user;
GRANT EXECUTE ON dbo.sp_CRUD_ActualizarCancion TO pm_app_user;
GRANT EXECUTE ON dbo.sp_CRUD_EliminarCancion TO pm_app_user;
GO
*/

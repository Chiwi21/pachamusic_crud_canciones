# =========================================================
# BASE DE DATOS II - Proyecto Integrador PachaMusicDB
# CRUD orientado a objetos para tabla dbo.Cancion
# Conexión SQL Server usando config.json
# Invocación de Store Procedures desde Python
# =========================================================

import json
import pyodbc


class GestorCanciones:
    """Clase que encapsula la conexión y las operaciones CRUD de canciones."""

    def __init__(self):
        """Inicializa la conexión leyendo los datos desde config.json."""
        try:
            with open("config.json", "r", encoding="utf-8") as archivo_config:
                config = json.load(archivo_config)

            name_server = config["name_server"]
            database = config["database"]
            username = config["username"]
            password = config["password"]
            controlador_odbc = config["controlador_odbc"]
            trust_server_certificate = config.get("trust_server_certificate", "yes")

            self.connection_string = (
                f"DRIVER={{{controlador_odbc}}};"
                f"SERVER={name_server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password};"
                f"TrustServerCertificate={trust_server_certificate};"
            )

            self.conexion = pyodbc.connect(self.connection_string)
            print("\nConexion exitosa a SQL Server - PachaMusicDB.\n")

        except FileNotFoundError:
            print("\nERROR: No se encontró el archivo config.json.\n")
            self.conexion = None
        except KeyError as e:
            print(f"\nERROR: Falta la clave {e} en config.json.\n")
            self.conexion = None
        except Exception as e:
            print("\nERROR al conectar con SQL Server:\n", e)
            self.conexion = None

    # -----------------------------------------------------
    # Métodos auxiliares
    # -----------------------------------------------------
    def _leer_entero(self, mensaje):
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("Ingrese un número entero válido.")

    def _leer_fecha_opcional(self, mensaje):
        fecha = input(mensaje).strip()
        if fecha == "":
            return None
        return fecha

    def _mostrar_resultado_sp(self, cursor):
        """Muestra la primera fila devuelta por un procedimiento, si existe."""
        try:
            fila = cursor.fetchone()
            if fila:
                print("\nResultado del procedimiento:")
                for indice, columna in enumerate(cursor.description):
                    print(f"{columna[0]}: {fila[indice]}")
        except Exception:
            pass

    # -----------------------------------------------------
    # CREATE
    # -----------------------------------------------------
    def insertar_cancion(self):
        try:
            print("\n\t\tINSERTAR NUEVA CANCION\n")

            id_album = self._leer_entero("Ingrese ID del album: \t")
            titulo_cancion = input("Ingrese titulo de la cancion: \t")
            duracion_segundos = self._leer_entero("Ingrese duracion en segundos: \t")
            estado_cancion = input("Ingrese estado (Activa/Inactiva): \t")
            fecha_publicacion = self._leer_fecha_opcional("Ingrese fecha publicacion YYYY-MM-DD o Enter si es NULL: \t")

            sentencia_sql = "{CALL dbo.sp_CRUD_CrearCancion (?, ?, ?, ?, ?)}"

            cursor = self.conexion.cursor()
            cursor.execute(
                sentencia_sql,
                (
                    id_album,
                    titulo_cancion,
                    duracion_segundos,
                    estado_cancion,
                    fecha_publicacion,
                ),
            )

            self._mostrar_resultado_sp(cursor)
            self.conexion.commit()
            cursor.close()
            print("\nOk ... Insercion finalizada.\n")

        except Exception as e:
            print("\nOcurrió un error al insertar la canción:\n", e)
            self.conexion.rollback()

    # -----------------------------------------------------
    # READ
    # -----------------------------------------------------
    def consultar_canciones(self):
        try:
            print("\n\t\tCONSULTA DE CANCIONES\n")
            valor = input("Ingrese ID de cancion o Enter para listar todas: \t").strip()
            id_cancion = int(valor) if valor != "" else None

            sentencia_sql = "{CALL dbo.sp_CRUD_ConsultarCanciones (?)}"

            cursor = self.conexion.cursor()
            cursor.execute(sentencia_sql, (id_cancion,))
            registros = cursor.fetchall()

            if len(registros) == 0:
                print("\nNo existen canciones para mostrar.\n")
            else:
                print("ID\tAlbum\tArtista\t\tTitulo\t\tDuracion\tEstado\tFecha\t\tRep\tLikes")
                print("-" * 130)

                for r in registros:
                    print(
                        f"{r[0]}\t"
                        f"{r[2]}\t"
                        f"{r[3]}\t"
                        f"{r[4]}\t"
                        f"{r[5]}\t\t"
                        f"{r[6]}\t"
                        f"{r[7]}\t"
                        f"{r[8]}\t"
                        f"{r[9]}"
                    )

                print("\nOk ... Consulta finalizada.\n")

            cursor.close()

        except ValueError:
            print("\nEl ID de canción debe ser numérico.\n")
        except Exception as e:
            print("\nOcurrió un error al consultar canciones:\n", e)

    # -----------------------------------------------------
    # UPDATE
    # -----------------------------------------------------
    def actualizar_cancion(self):
        try:
            print("\n\t\tACTUALIZAR CANCION\n")

            id_cancion = self._leer_entero("Ingrese ID de la cancion a actualizar: \t")
            id_album = self._leer_entero("Ingrese nuevo ID del album: \t")
            titulo_cancion = input("Ingrese nuevo titulo de la cancion: \t")
            duracion_segundos = self._leer_entero("Ingrese nueva duracion en segundos: \t")
            estado_cancion = input("Ingrese nuevo estado (Activa/Inactiva): \t")
            fecha_publicacion = self._leer_fecha_opcional("Ingrese nueva fecha YYYY-MM-DD o Enter si es NULL: \t")

            sentencia_sql = "{CALL dbo.sp_CRUD_ActualizarCancion (?, ?, ?, ?, ?, ?)}"

            cursor = self.conexion.cursor()
            cursor.execute(
                sentencia_sql,
                (
                    id_cancion,
                    id_album,
                    titulo_cancion,
                    duracion_segundos,
                    estado_cancion,
                    fecha_publicacion,
                ),
            )

            self._mostrar_resultado_sp(cursor)
            self.conexion.commit()
            cursor.close()
            print("\nOk ... Actualizacion finalizada.\n")

        except Exception as e:
            print("\nOcurrió un error al actualizar la canción:\n", e)
            self.conexion.rollback()

    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------
    def eliminar_cancion(self):
        try:
            print("\n\t\tELIMINAR CANCION\n")

            id_cancion = self._leer_entero("Ingrese ID de la cancion a eliminar: \t")
            confirmacion = input("¿Está seguro? S/N: \t")

            if confirmacion.upper() != "S":
                print("\nEliminacion cancelada.\n")
                return

            sentencia_sql = "{CALL dbo.sp_CRUD_EliminarCancion (?)}"

            cursor = self.conexion.cursor()
            cursor.execute(sentencia_sql, (id_cancion,))

            self._mostrar_resultado_sp(cursor)
            self.conexion.commit()
            cursor.close()
            print("\nOk ... Eliminacion finalizada.\n")

        except Exception as e:
            print("\nOcurrió un error al eliminar la canción:\n", e)
            self.conexion.rollback()

    # -----------------------------------------------------
    # Menú CRUD
    # -----------------------------------------------------
    def ejecutar_menu(self):
        if self.conexion is None:
            print("No se puede ejecutar el menú porque no existe conexión.")
            return

        while True:
            print("\n\t**************************************")
            print("\t** SISTEMA CRUD PACHAMUSIC - CANCION **")
            print("\t**************************************")
            print("\t1. Crear canción")
            print("\t2. Consultar canciones")
            print("\t3. Actualizar canción")
            print("\t4. Eliminar canción")
            print("\t5. Salir\n")

            opcion = input("Seleccione una opción 1-5: \t")

            if opcion == "1":
                self.insertar_cancion()
            elif opcion == "2":
                self.consultar_canciones()
            elif opcion == "3":
                self.actualizar_cancion()
            elif opcion == "4":
                self.eliminar_cancion()
            elif opcion == "5":
                print("\nSaliendo del programa...\n")
                break
            else:
                print("\nOpción no válida. Intente nuevamente.\n")

    def cerrar_conexion(self):
        try:
            if self.conexion is not None:
                self.conexion.close()
                print("Conexion cerrada.\n")
        except Exception as e:
            print("No se pudo cerrar la conexión:\n", e)


# =========================================================
# Programa principal
# =========================================================
if __name__ == "__main__":
    gestor = GestorCanciones()
    try:
        gestor.ejecutar_menu()
    finally:
        gestor.cerrar_conexion()

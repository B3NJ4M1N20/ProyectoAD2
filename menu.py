import campus
import datos
import versiones_anteriores.gestion_dispositivos as gestion_dispositivos
from github import BadCredentialsException, RateLimitExceededException, UnknownObjectException
import json
import os

class Menu:
    def __init__(self, datos_actuales, campus_manager, device_manager):
        self.datos_actuales = datos_actuales
        self.campus_manager = campus_manager
        self.device_manager = device_manager

    def mostrar_menu(self):
        ejecutando = True
        archivo_actual = None

        while ejecutando:
            print("\n--- Menú ---")
            for opcion, metodo in self.opciones.items():
                print(f"{opcion}. {metodo.__name__.replace('_', ' ').capitalize()}")

            opcion = self.obtener_opcion_valida()

            if opcion == 1:  # Crear archivo
                nombre_archivo = input("Ingrese el nombre del archivo: ")
                archivo_actual = os.path.join("archivos_de_red", nombre_archivo + ".json")
                try:
                    self.datos_actuales = datos.Datos.cargar_datos(archivo_actual)
                    print(f"Archivo de red '{archivo_actual}' creado exitosamente.")
                except IOError as e:
                    print(f"Error al crear el archivo: {e}")
            elif opcion == 2:  # Cargar archivo
                archivo_actual = self._cargar_archivo_red()
                if archivo_actual:
                    self.datos_actuales = datos.Datos.cargar_datos(archivo_actual)
            elif opcion == 14:  # Salir
                self.preguntar_guardar()  # Preguntar antes de salir
                self.salir()
            else:
                try:
                    self.opciones[opcion](self)  # Pasar self como argumento
                except ValueError as e:
                    print(f"Error de valor: {e}. Por favor, ingrese un número válido.")
                except FileNotFoundError as e:
                    print(f"Error: Archivo no encontrado: {e}")
                except datos.CampusNoEncontrado as e:
                    print(f"Error: Campus no encontrado: {e}")
                except gestion_dispositivos.DispositivoNoEncontrado as e:
                    print(f"Error: Dispositivo no encontrado: {e}")
                except json.JSONDecodeError as e:
                    print(f"Error: El archivo no tiene un formato JSON válido: {e}")
                except BadCredentialsException as e:
                    print(f"Error de credenciales de GitHub: {e}")
                except RateLimitExceededException as e:
                    print(f"Límite de tasa de GitHub excedido: {e}")
                except UnknownObjectException as e:
                    print(f"Objeto no encontrado en GitHub: {e}")
                except Exception as e:
                    print(f"Error inesperado: {e}")

    def obtener_opcion_valida(self):
        while True:
            try:
                opcion = int(input("Seleccione una opción: "))
                if opcion in self.opciones:
                    return opcion
                else:
                    raise ValueError("Opción inválida.")
            except ValueError:
                print("Error: Ingrese un número válido.")

    def salir(self):
        print("Saliendo...")
        exit()

    def _cargar_archivo_red(self):
        archivos = [f for f in os.listdir("archivos_de_red") if f.endswith(".json")]
        if not archivos:
            print("No hay archivos de red disponibles.")
            return None

        print("Archivos disponibles:")
        for i, archivo in enumerate(archivos):
            print(f"{i+1}. {archivo}")

        while True:
            try:
                indice = int(input("Seleccione un archivo (o 0 para cancelar): ")) - 1
                if 0 <= indice < len(archivos):
                    archivo_seleccionado = os.path.join("archivos_de_red", archivos[indice])
                    with open(archivo_seleccionado, 'r') as f:
                        json.load(f)
                    self.datos_actuales.archivo_actual = archivo_seleccionado
                    return archivo_seleccionado
                elif indice == -1:
                    return None
                else:
                    raise ValueError("Índice inválido.")
            except (ValueError, json.JSONDecodeError) as e:
                print(f"Error: No se pudo cargar el archivo. Asegúrese de que sea un archivo JSON válido: {e}")

    def preguntar_guardar(self):
        if self.datos_actuales.cambios_pendientes:
            confirmacion = input("¿Desea guardar los cambios? (s/n): ")
            if confirmacion.lower() == 's':
                self.datos_actuales.guardar_datos()
                print("Cambios guardados exitosamente.")

    def _crear_campus(self):
        self.campus_manager.crear_campus()
        self.preguntar_guardar()

    def _modificar_campus(self):
        self.campus_manager.modificar_campus()
        self.preguntar_guardar()

    def _eliminar_campus(self):
        self.campus_manager.eliminar_campus()
        self.preguntar_guardar()

    def _listar_campus(self):
        self.campus_manager.listar_campus()

    def _crear_dispositivo(self):
        self.device_manager.crear_dispositivo()
        self.preguntar_guardar()

    def _modificar_dispositivo(self):
        self.device_manager.modificar_dispositivo()
        self.preguntar_guardar()

    def _eliminar_dispositivo(self):
        self.device_manager.eliminar_dispositivo()
        self.preguntar_guardar()

    def _listar_dispositivos(self):
        self.device_manager.listar_dispositivos()

    def _configurar_dispositivo(self):
        self.device_manager.configurar_dispositivo()
        self.preguntar_guardar()

    def _subir_archivo_github(self):
        if self.datos_actuales.archivo_actual:
            try:
                self.datos_actuales.crear_archivo_red_github()
                print("Archivo de red subido a GitHub exitosamente.")
            except (json.JSONDecodeError, BadCredentialsException, RateLimitExceededException, UnknownObjectException) as e:
                print(f"Error al subir archivo de red a GitHub: {e}")
        else:
            print("No hay ningún archivo cargado para subir.")

    opciones = {
        1: _cargar_archivo_red,
        2: _cargar_archivo_red,
        3: _crear_campus,
        4: _modificar_campus,
        5: _eliminar_campus,
        6: _crear_dispositivo,
        7: _modificar_dispositivo,
        8: _eliminar_dispositivo,
        9: _listar_campus,
        10: _listar_dispositivos,
        11: _configurar_dispositivo,
        14: salir
    }

if __name__ == "__main__":
    datos_actuales = datos.Datos()
    campus_manager = campus.CampusManager(datos_actuales)
    device_manager = gestion_dispositivos.DeviceManager(datos_actuales)
    menu = Menu(datos_actuales, campus_manager, device_manager)
    menu.mostrar_menu()
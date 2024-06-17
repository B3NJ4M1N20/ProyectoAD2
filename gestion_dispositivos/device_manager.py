from dispositivos import Dispositivo, validar_nombre
from campus import CampusManager
from excepciones import DispositivoNoEncontrado, DispositivoYaExisteEnCampus

class DeviceManager:
    def __init__(self, datos_actuales):
        self.dispositivos = {}
        self.datos_actuales = datos_actuales

    def crear_dispositivo(self):
        if not self.datos_actuales.campus:
            print("No hay campus creados. Debe crear un campus antes de agregar un dispositivo.")
            if input("¿Desea crear un campus ahora? (s/n): ").lower() == 's':
                CampusManager(self.datos_actuales).crear_campus()  # Pasar self.datos_actuales al constructor
                return
            else:
                return

        while True:
            tipo = input("Tipo de dispositivo (router/switch): ").lower()
            if tipo in ["router", "switch"]:
                break
            else:
                print("Tipo de dispositivo inválido. Ingrese 'router' o 'switch'.")

        nombre = validar_nombre(input("Nombre del dispositivo: "), self.datos_actuales)
        descripcion = input("Descripción del dispositivo: ")

        CampusManager(self.datos_actuales).listar_campus()  # Pasar self.datos_actuales al constructor
        while True:
            campus_id = input("ID del campus al que pertenece (o 'c' para cancelar): ")
            if campus_id.lower() == 'c':
                return
            if campus_id not in self.datos_actuales.campus:
                print("Campus no encontrado. Intente de nuevo.")
            else:
                break

        nuevo_dispositivo = Dispositivo(tipo, nombre, descripcion, campus_id)
        try:
            self.datos_actuales.agregar_dispositivo(nuevo_dispositivo)
            self.dispositivos[nuevo_dispositivo.id] = nuevo_dispositivo
            print("Dispositivo creado exitosamente.")
        except ValueError as e:
            print(e)
        except DispositivoYaExisteEnCampus as e:
            print(e)

    def modificar_dispositivo(self):
        self.listar_dispositivos()
        id_dispositivo = input("ID del dispositivo a modificar (o 'c' para cancelar): ")
        if id_dispositivo.lower() == 'c':
            return

        dispositivo_encontrado = self.dispositivos.get(id_dispositivo)
        if not dispositivo_encontrado:
            raise DispositivoNoEncontrado("Dispositivo no encontrado.")

        print(f"Modificando {dispositivo_encontrado}")

        nuevo_nombre = validar_nombre(input("Nuevo nombre (opcional): "), self.datos_actuales)
        if nuevo_nombre:
            dispositivo_encontrado.nombre = nuevo_nombre

        nueva_descripcion = input("Nueva descripción (opcional): ")
        if nueva_descripcion:
            dispositivo_encontrado.descripcion = nueva_descripcion

        CampusManager(self.datos_actuales).listar_campus()
        while True:
            nuevo_campus_id = input("Nuevo campus ID (opcional, ingrese el ID): ")
            if nuevo_campus_id:
                if nuevo_campus_id not in self.datos_actuales.campus:
                    print("Campus no encontrado. Intente de nuevo.")
                else:
                    dispositivo_encontrado.campus_id = nuevo_campus_id
                    break
            else:
                break

        self.datos_actuales.guardar_datos()
        print("Dispositivo modificado exitosamente.")

    def eliminar_dispositivo(self):
        self.listar_dispositivos()
        id_dispositivo = input("ID del dispositivo a eliminar (o 'c' para cancelar): ")
        if id_dispositivo.lower() == 'c':
            return

        try:
            del self.dispositivos[id_dispositivo]
            self.datos_actuales.eliminar_dispositivo(id_dispositivo)
            print("Dispositivo eliminado exitosamente.")
        except KeyError:
            print("Dispositivo no encontrado.")
        except DispositivoNoEncontrado as e:
            print(e)

    def listar_dispositivos(self):
        if self.dispositivos:
            print("Dispositivos:")
            for dispositivo in self.dispositivos.values():
                print(dispositivo)
                if input(f"¿Desea ver la configuración de '{dispositivo.nombre}'? (s/n): ").lower() == 's':
                    for clave, valor in dispositivo.configuracion.items():
                        print(f"    - {clave}: {valor}")
        else:
            print("No hay dispositivos registrados.")

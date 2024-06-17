import re
import uuid
from excepciones import CampusNoEncontrado, DispositivoYaExisteEnCampus

class Campus:
    def __init__(self, nombre, descripcion="", id=None, tipo="No especificado"):
        self.nombre = nombre
        self.descripcion = descripcion
        self.dispositivos = []
        self.id = id or str(uuid.uuid4())  # Asignar un UUID si no se proporciona un ID
        self.tipo = tipo

    def __str__(self):
        return f"ID: {self.id}\nNombre: {self.nombre}\nDescripción: {self.descripcion}\nTipo: {self.tipo}\nDispositivos: {len(self.dispositivos)}"

    def agregar_dispositivo(self, dispositivo):
        if dispositivo in self.dispositivos:
            raise DispositivoYaExisteEnCampus("El dispositivo ya existe en este campus.")
        else:
            self.dispositivos.append(dispositivo)

def validar_nombre(nombre, datos_actuales):
    while True:
        if not nombre:
            print("El nombre no puede estar vacío.")
        elif not re.match("^[a-zA-Z0-9_-]+$", nombre):
            print("El nombre solo puede contener caracteres alfanuméricos, guiones bajos y guiones medios.")
        elif len(nombre) > 50:
            print("El nombre no puede tener más de 50 caracteres.")
        elif any(campus.nombre == nombre for campus in datos_actuales.campus.values()):
            print("Ya existe un campus con ese nombre.")
        else:
            return nombre
        nombre = input("Nombre del campus: ")

class CampusManager:
    def __init__(self, datos_actuales):
        self.campus = {}
        self.datos_actuales = datos_actuales

    def crear_campus(self):
        while True:
            try:
                id_campus = input("ID del campus: ")
                if not id_campus:
                    raise ValueError("El ID del campus no puede estar vacío.")
                if not re.match("^[a-zA-Z0-9_-]+$", id_campus):
                    raise ValueError("El ID del campus solo puede contener caracteres alfanuméricos, guiones bajos y guiones medios.")
                if id_campus in self.campus:
                    raise ValueError("Ya existe un campus con ese ID.")
                break
            except ValueError as e:
                print(f"Error: {e}")

        nombre = validar_nombre(input("Nombre del campus: "), self.datos_actuales)
        descripcion = input("Descripción del campus: ")

        while True:
            print("\nJerarquía del campus:")
            print("1. Core")
            print("2. Distribución")
            print("3. Acceso")
            try:
                jerarquia = int(input("Seleccione una opción: "))
                if 1 <= jerarquia <= 3:
                    jerarquia = ["Core", "Distribución", "Acceso"][jerarquia - 1]
                    break
                else:
                    raise ValueError("Opción inválida.")
            except ValueError as e:
                print(f"Error: {e}")

        nuevo_campus = Campus(nombre, descripcion, id=id_campus, tipo=jerarquia)
        self.campus[nuevo_campus.id] = nuevo_campus
        self.datos_actuales.agregar_campus(nuevo_campus)
        print(f"Campus '{nombre}' creado exitosamente.")

    def modificar_campus(self):
        self.listar_campus()
        id_campus = input("ID del campus a modificar (o 'c' para cancelar): ")
        if id_campus.lower() == 'c':
            return

        campus_a_modificar = self.campus.get(id_campus)
        if campus_a_modificar:
            nuevo_nombre = validar_nombre(input("Nuevo nombre (opcional): "), self.datos_actuales)
            if nuevo_nombre:
                campus_a_modificar.nombre = nuevo_nombre
            nueva_descripcion = input("Nueva descripción (opcional): ")
            if nueva_descripcion:
                campus_a_modificar.descripcion = nueva_descripcion
            while True:
                nuevo_tipo = input("Nueva jerarquía (opcional, ingrese Core/Distribución/Acceso): ").lower()
                if nuevo_tipo in ["core", "distribucion", "acceso", ""]:
                    if nuevo_tipo:
                        campus_a_modificar.tipo = nuevo_tipo.capitalize()  # Capitalizar la primera letra
                    break
                else:
                    print("Jerarquía inválida. Por favor, ingrese 'Core', 'Distribución' o 'Acceso'.")
            print("Campus modificado exitosamente.")
        else:
            print("Campus no encontrado.")

    def eliminar_campus(self):
        self.listar_campus()
        id_campus = input("ID del campus a eliminar (o 'c' para cancelar): ")
        if id_campus.lower() == 'c':
            return

        try:
            del self.campus[id_campus]
            print("Campus eliminado exitosamente.")
        except KeyError:
            print(f"Campus con ID '{id_campus}' no encontrado.")

    def listar_campus(self):
        if self.campus:
            print("Campus:")
            for campus in self.campus.values():
                print(campus)
        else:
            print("No hay campus registrados.")
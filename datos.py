import json
import os
import uuid
from campus import Campus
from versiones_anteriores.gestion_dispositivos import Dispositivo
from excepciones import CampusNoEncontrado, DispositivoNoEncontrado

class Datos:
    def __init__(self):
        self.campus = {}
        self.dispositivos = {}
        self.archivo_actual = None
        self.cambios_pendientes = False

    @classmethod
    def cargar_datos(cls, archivo):
        datos = cls()
        datos.archivo_actual = archivo
        try:
            with open(archivo, 'r') as f:
                datos_json = json.load(f)

                for campus_data in datos_json.get("campus", []):
                    if not all(key in campus_data for key in ["nombre", "id", "tipo"]):
                        raise ValueError("Faltan campos obligatorios en los datos del campus.")
                    if not isinstance(campus_data["nombre"], str) or not isinstance(campus_data["id"], str) or not isinstance(campus_data["tipo"], str):
                        raise TypeError("Tipo de datos incorrecto en los datos del campus.")
                    campus = Campus(**campus_data)
                    datos.campus[campus.id] = campus

                for dispositivo_data in datos_json.get("dispositivos", []):
                    if not all(key in dispositivo_data for key in ["tipo", "nombre", "campus_id", "id"]):
                        raise ValueError("Faltan campos obligatorios en los datos del dispositivo.")
                    if not isinstance(dispositivo_data["tipo"], str) or not isinstance(dispositivo_data["nombre"], str) or not isinstance(dispositivo_data["campus_id"], str) or not isinstance(dispositivo_data["id"], str):
                        raise TypeError("Tipo de datos incorrecto en los datos del dispositivo.")
                    campus = datos.campus.get(dispositivo_data["campus_id"])
                    if not campus:
                        raise ValueError(f"El campus_id '{dispositivo_data['campus_id']}' no existe.")
                    dispositivo = Dispositivo(**dispositivo_data, campus=campus)
                    datos.dispositivos[dispositivo.id] = dispositivo
        except FileNotFoundError:
            print(f"El archivo '{archivo}' no existe. Se creará uno nuevo.")
            with open(archivo, 'w') as f:  # Crear el archivo si no existe
                json.dump({"campus": [], "dispositivos": []}, f, indent=4)
        except json.JSONDecodeError:
            print(f"Error: El archivo '{archivo}' no tiene un formato JSON válido.")
            datos.campus = {}
            datos.dispositivos = {}
        except (ValueError, TypeError) as e:
            print(f"Error al cargar los datos: {e}")
            datos.campus = {}
            datos.dispositivos = {}

        return datos

    def guardar_datos(self, archivo=None):
        if archivo is None:
            archivo = self.archivo_actual

        if archivo:
            datos_json = {
                "campus": [
                    {
                        "nombre": campus.nombre,
                        "descripcion": campus.descripcion,
                        "id": campus.id,
                        "tipo": campus.tipo
                    } for campus in self.campus.values()
                ],
                "dispositivos": [
                    {
                        "tipo": dispositivo.tipo,
                        "nombre": dispositivo.nombre,
                        "descripcion": dispositivo.descripcion,
                        "campus_id": dispositivo.campus_id if dispositivo.campus_id else None,
                        "id": dispositivo.id,
                        "configuracion": dispositivo.configuracion
                    } for dispositivo in self.dispositivos.values()
                ]
            }
            try:
                with open(archivo, 'w') as f:
                    json.dump(datos_json, f, indent=4)
                self.cambios_pendientes = False
                print(f"Datos guardados en '{archivo}'")
            except IOError as e:
                print(f"Error al guardar el archivo: {e}")
        else:
            print("No hay ningún archivo cargado para guardar.")

    def agregar_campus(self, campus):
        if campus.id in self.campus:
            raise ValueError(f"El campus con ID '{campus.id}' ya existe.")
        self.campus[campus.id] = campus
        self.cambios_pendientes = True

    def eliminar_campus(self, id_campus):
        if id_campus in self.campus:
            del self.campus[id_campus]
            self.dispositivos = {nombre: disp for nombre, disp in self.dispositivos.items() if disp.campus_id != id_campus}
            self.cambios_pendientes = True
        else:
            raise CampusNoEncontrado(f"Campus con ID '{id_campus}' no encontrado.")

    def agregar_dispositivo(self, dispositivo):
        if dispositivo.id in self.dispositivos:
            raise ValueError(f"El dispositivo con ID '{dispositivo.id}' ya existe.")
        self.dispositivos[dispositivo.id] = dispositivo
        self.cambios_pendientes = True

    def eliminar_dispositivo(self, id_dispositivo):
        if id_dispositivo in self.dispositivos:
            del self.dispositivos[id_dispositivo]
            self.cambios_pendientes = True
        else:
            raise DispositivoNoEncontrado(f"Dispositivo con ID '{id_dispositivo}' no encontrado.")

    def cargar_configuracion(self, dispositivo_id):
        dispositivo = next((d for d in self.dispositivos.values() if d.id == dispositivo_id), None)
        if dispositivo:
            return dispositivo.configuracion
        else:
            return {}

    def guardar_configuracion(self, dispositivo_id, configuracion):
        dispositivo = next((d for d in self.dispositivos.values() if d.id == dispositivo_id), None)
        if dispositivo:
            dispositivo.configuracion = configuracion
            self.cambios_pendientes = True

    def crear_archivo_red_github(self):
        pass

    def cambios_pendientes(self):
        return self.cambios_pendientes
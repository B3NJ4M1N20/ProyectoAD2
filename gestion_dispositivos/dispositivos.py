import uuid

class Dispositivo:
    def __init__(self, tipo, nombre, descripcion="", campus_id=None, id=None, configuracion=None):
        self.tipo = tipo
        self.nombre = nombre
        self.descripcion = descripcion
        self.campus_id = campus_id
        self.id = id or str(uuid.uuid4())  # Asignar un UUID si no se proporciona un ID
        self.configuracion = configuracion or {}

    def __str__(self):
        return f"ID: {self.id}\nNombre: {self.nombre}\nTipo: {self.tipo}\nDescripción: {self.descripcion}\nCampus ID: {self.campus_id}"

def validar_ip(ip):
    octetos = ip.split(".")
    if len(octetos) != 4:
        return False
    for octeto in octetos:
        try:
            if not (0 <= int(octeto) <= 255):
                return False
        except ValueError:
            return False
    return True

def validar_mascara_red(mascara):
    octetos = mascara.split(".")
    if len(octetos) != 4:
        return False
    try:
        bits = [bin(int(x))[2:].zfill(8) for x in octetos]
        mascara_binaria = "".join(bits)
        return mascara_binaria.startswith("1"*mascara_binaria.rfind("0")) and mascara_binaria.endswith("0"*(32-mascara_binaria.rfind("0")))
    except ValueError:
        return False

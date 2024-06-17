import json

def cargar_datos():
    try:
        with open("red.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"campus": [], "dispositivos": []}

def guardar_datos(datos):
    with open("red.json", "w") as f:
        json.dump(datos, f, indent=4)

def crear_campus():
    nombre = input("Nombre del campus: ")
    while not nombre:  # Validar que el nombre no esté vacío
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre del campus: ")

    descripcion = input("Descripción (opcional): ")

    datos["campus"].append({"nombre": nombre, "descripcion": descripcion, "dispositivos": []})
    guardar_datos(datos)
    print("Campus creado exitosamente.")

def modificar_campus():
    nombre = input("Nombre del campus a modificar: ")
    for campus in datos["campus"]:
        if campus["nombre"] == nombre:
            campus["descripcion"] = input("Nueva descripción (opcional): ")
            guardar_datos(datos)
            print("Campus modificado exitosamente.")
            return
    print("Campus no encontrado.")

def eliminar_campus():
    nombre = input("Nombre del campus a eliminar: ")
    for i, campus in enumerate(datos["campus"]):
        if campus["nombre"] == nombre:
            del datos["campus"][i]
            guardar_datos(datos)
            print("Campus eliminado exitosamente.")
            return
    print("Campus no encontrado.")

def crear_dispositivo():
    tipos = ["Router", "Switch", "Switch Multicapa"]
    print("Tipos de dispositivos:")
    for i, tipo in enumerate(tipos):
        print(f"{i+1}. {tipo}")
    tipo_index = int(input("Seleccione el tipo de dispositivo: ")) - 1
    while tipo_index not in range(len(tipos)):
        print("Opción inválida.")
        tipo_index = int(input("Seleccione el tipo de dispositivo: ")) - 1
    
    nombre = input("Nombre del dispositivo: ")
    while not nombre:
        print("El nombre no puede estar vacío.")
        nombre = input("Nombre del dispositivo: ")

    campus_nombre = input("Nombre del campus al que pertenece: ")
    for campus in datos["campus"]:
        if campus["nombre"] == campus_nombre:
            campus["dispositivos"].append({"tipo": tipos[tipo_index], "nombre": nombre})
            guardar_datos(datos)
            print("Dispositivo creado exitosamente.")
            return
    print("Campus no encontrado. ¿Desea crear uno nuevo? (S/N): ")
    if input().upper() == "S":
        crear_campus()
        crear_dispositivo()  # Volver a intentar crear el dispositivo después de crear el campus

def modificar_dispositivo():
    nombre = input("Nombre del dispositivo a modificar: ")
    for campus in datos["campus"]:
        for i, dispositivo in enumerate(campus["dispositivos"]):
            if dispositivo["nombre"] == nombre:
                nuevo_nombre = input("Nuevo nombre (opcional): ")
                if nuevo_nombre:
                    dispositivo["nombre"] = nuevo_nombre
                guardar_datos(datos)
                print("Dispositivo modificado exitosamente.")
                return
    print("Dispositivo no encontrado.")

def eliminar_dispositivo():
    nombre = input("Nombre del dispositivo a eliminar: ")
    for campus in datos["campus"]:
        for i, dispositivo in enumerate(campus["dispositivos"]):
            if dispositivo["nombre"] == nombre:
                del campus["dispositivos"][i]
                guardar_datos(datos)
                print("Dispositivo eliminado exitosamente.")
                return
    print("Dispositivo no encontrado.")

def listar_campus():
    if not datos["campus"]:
        print("No hay campus creados.")
        return
    print("\n--- Lista de Campus ---")
    for campus in datos["campus"]:
        print(f"Nombre: {campus['nombre']}")
        print(f"Descripción: {campus['descripcion']}")
        print(f"Dispositivos asociados: {', '.join(d['nombre'] for d in campus['dispositivos'])}")
        print("-" * 20)

def listar_dispositivos():
    if not any(campus["dispositivos"] for campus in datos["campus"]):
        print("No hay dispositivos creados.")
        return
    print("\n--- Lista de Dispositivos ---")
    for campus in datos["campus"]:
        for dispositivo in campus["dispositivos"]:
            print(f"Nombre: {dispositivo['nombre']}")
            print(f"Tipo: {dispositivo['tipo']}")
            print(f"Campus: {campus['nombre']}")
            print("-" * 20)

def configurar_dispositivo():
    nombre = input("Nombre del dispositivo a configurar: ")
    for campus in datos["campus"]:
        for dispositivo in campus["dispositivos"]:
            if dispositivo["nombre"] == nombre:
                print(f"\nConfigurando {dispositivo['tipo']} - {nombre}")

                # Configuración inicial
                hostname = input("Hostname: ") or nombre  # Usar nombre si no se ingresa nada
                password = input("Password: ")
                jerarquia = input("Jerarquía (1. Core, 2. Distribución, 3. Acceso): ") or "3" # Default a Acceso

                # Configuración avanzada (opcional)
                config_avanzada = input("¿Desea continuar con la configuración avanzada? (S/N): ").upper()
                if config_avanzada == "S":
                    dns = input("DNS (opcional): ")
                    dhcp = input("DHCP (opcional): ")

                    # Configuración de interfaz
                    interfaz = input(f"Interfaz a configurar (ej. 0/0, 0/1): ")
                    ipv4 = input("Dirección IPv4 (opcional): ")
                    mascara = input("Máscara de red (opcional): ")
                    protocolos = []
                    if dispositivo["tipo"] in ["Router", "Switch Multicapa"]:
                        protocolos_str = input("Protocolos de enrutamiento (OSPF, EIGRP, separados por coma): ")
                        protocolos = [p.strip() for p in protocolos_str.split(",")] if protocolos_str else []
                    vlan_nombre = input("Nombre de VLAN (opcional): ")
                    vlan_id = input("VLAN ID (opcional): ")

                    # Guardar configuración avanzada
                    dispositivo["configuracion"] = {
                        "hostname": hostname,
                        "password": password,
                        "jerarquia": jerarquia,
                        "dns": dns,
                        "dhcp": dhcp,
                        "interfaces": {
                            interfaz: {
                                "ipv4": ipv4,
                                "mascara": mascara,
                                "protocolos": protocolos,
                                "vlan_nombre": vlan_nombre,
                                "vlan_id": vlan_id
                            }
                        }
                    }
                else:
                    # Guardar solo configuración básica
                    dispositivo["configuracion"] = {
                        "hostname": hostname,
                        "password": password,
                        "jerarquia": jerarquia
                    }

                guardar_datos(datos)
                print("Dispositivo configurado exitosamente.")
                return
    print("Dispositivo no encontrado.")
    
# Menú principal y bucle
datos = cargar_datos()
while True:
    print("\n--- Menú ---")
    print("1. Crear campus")
    print("2. Modificar campus")
    print("3. Eliminar campus")
    print("4. Crear dispositivo")
    print("5. Modificar dispositivo")
    print("6. Eliminar dispositivo")
    print("7. Listar campus")
    print("8. Listar dispositivos")
    print("9. Configurar dispositivo")
    print("10. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        crear_campus()
    elif opcion == "2":
        modificar_campus()
    elif opcion == "3":
        eliminar_campus()
    elif opcion == "4":
        crear_dispositivo()
    elif opcion == "5":
        modificar_dispositivo()
    elif opcion == "6":
        eliminar_dispositivo()
    elif opcion == "7":
        listar_campus()
    elif opcion == "8":
        listar_dispositivos()
    elif opcion == "9":
        configurar_dispositivo()  # Implementar esta función
    elif opcion == "10":
        print("Saliendo...")
        break
    else:
        print("Opción inválida.")

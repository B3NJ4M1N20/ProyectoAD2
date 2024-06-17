from dispositivos import validar_ip, validar_mascara_red
from device_manager import DeviceManager

class DeviceManager(DeviceManager):  # Herencia de DeviceManager
    def configurar_dispositivo(self):
        self.listar_dispositivos()
        id_dispositivo = input("ID del dispositivo a configurar (o 'c' para cancelar): ")
        if id_dispositivo.lower() == 'c':
            return

        dispositivo = self.dispositivos.get(id_dispositivo)
        if not dispositivo:
            print("Dispositivo no encontrado.")
            return

        while True:
            print("\n--- Configuración de Dispositivo ---")
            print("1. Modificar configuración inicial")
            print("2. Modificar configuración avanzada")
            print("3. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.configurar_inicial(dispositivo)
            elif opcion == '2':
                self.configurar_avanzada(dispositivo)
            elif opcion == '3':
                break
            else:
                print("Opción inválida.")

    def configurar_inicial(self, dispositivo):
        hostname = input("Hostname (opcional): ")
        if hostname:
            dispositivo.configuracion["hostname"] = hostname

        while True:
            password = input("Password (opcional): ")
            if not password:
                break
            confirmacion = input("Confirmar password: ")
            if password == confirmacion:
                dispositivo.configuracion["password"] = password
                break
            else:
                print("Las contraseñas no coinciden.")

        self.datos_actuales.guardar_datos()
        print("Configuración inicial guardada.")

    def configurar_avanzada(self, dispositivo):
        while True:
            print("\n--- Configuración Avanzada ---")
            print("1. Interfaces")
            print("2. Servicios")
            print("3. Guardar configuración")
            print("4. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.configurar_interfaces(dispositivo)
            elif opcion == '2':
                self.configurar_servicios(dispositivo)
            elif opcion == '3':
                self.datos_actuales.guardar_datos()
                print("Configuración avanzada guardada.")
            elif opcion == '4':
                break
            else:
                print("Opción inválida.")

    def configurar_interfaces(self, dispositivo):
        interfaces_disponibles = {
            "router": {
                "Ethernet0/1": {},
                "Ethernet0/2": {},
                "Ethernet0/3": {},
                "Ethernet0/4": {},
                "Ethernet0/5": {},
                "Ethernet0/6": {},
                "Ethernet0/7": {},
                "Ethernet0/8": {},
                "Ethernet0/9": {},
            },
            "switch": {
                "Ethernet0/1": {},
                "Ethernet0/2": {},
                "Ethernet0/1": {},
                "Ethernet0/2": {},
                "Ethernet0/3": {},
                "Ethernet0/4": {},
                "Ethernet0/5": {},
                "Ethernet0/6": {},
                "Ethernet0/7": {},
                "Ethernet0/8": {},
                "Ethernet0/9": {},
                "Ethernet0/10": {},
                "Ethernet0/12": {},
                "Ethernet0/13": {},
                "Ethernet0/14": {},
                "Ethernet0/15": {},
                "Ethernet0/16": {},
                "Ethernet0/17": {},
                "Ethernet0/18": {},
                "Ethernet0/19": {},     
                "Ethernet0/20": {},
                "Ethernet0/21": {},
                "Ethernet0/22": {},
                "Ethernet0/23": {},
                "Ethernet0/24": {},                                           
            }
        }

        while True:
            print("\n--- Configuración de Interfaces ---")
            for i, interfaz in enumerate(interfaces_disponibles[dispositivo.tipo]):
                print(f"{i+1}. {interfaz}")
            print(f"{len(interfaces_disponibles[dispositivo.tipo])+1}. Salir")

            try:
                opcion = int(input("Seleccione una interfaz: ")) - 1
                if 0 <= opcion < len(interfaces_disponibles[dispositivo.tipo]):
                    nombre_interfaz = list(interfaces_disponibles[dispositivo.tipo].keys())[opcion]
                    self.configurar_interfaz(dispositivo, nombre_interfaz)
                elif opcion == len(interfaces_disponibles[dispositivo.tipo]):
                    break
                else:
                    raise ValueError("Opción inválida.")
            except ValueError:
                print("Ingrese un número válido.")

    def configurar_interfaz(self, dispositivo, nombre_interfaz):
        if dispositivo.tipo == "router":
            descripcion = input("Descripción (opcional): ")
            while True:
                ip_address = input("Dirección IP (formato x.x.x.x): ")
                if not ip_address:
                    break
                if not validar_ip(ip_address):
                    print("Dirección IP inválida. Intente de nuevo.")
                    continue

                while True:
                    mascara_red = input("Máscara de red (formato x.x.x.x): ")
                    if not mascara_red:
                        break
                    if not validar_mascara_red(mascara_red):
                        print("Máscara de red inválida. Intente de nuevo.")
                        continue

                    dispositivo.configuracion[nombre_interfaz] = {
                        "description": descripcion,
                        "ip address": f"{ip_address} {mascara_red}"
                    }

                    if input("¿Desea agregar MPLS? (s/n): ").lower() == 's':
                        dispositivo.configuracion[nombre_interfaz]["mpls ip"] = ""  # Placeholder para MPLS

                    self.datos_actuales.guardar_datos()
                    print(f"Interfaz {nombre_interfaz} configurada exitosamente.")
                    break
        elif dispositivo.tipo == "switch":
            # Configuración para switch
            while True:
                print("\nOpciones de configuración:")
                print("1. switchport mode access")
                print("2. switchport mode trunk")
                print("3. Salir")

                opcion = input("Seleccione una opción: ")

                if opcion == '1':
                    while True:
                        vlan = input("Ingrese el número de VLAN (o 'c' para cancelar): ")
                        if vlan.lower() == 'c':
                            break
                        try:
                            vlan = int(vlan)
                            if 1 <= vlan <= 4094:  # Rango válido de VLANs
                                dispositivo.configuracion[nombre_interfaz] = {
                                    "switchport mode": "access",
                                    "switchport access vlan": vlan
                                }
                                self.datos_actuales.guardar_datos()
                                print(f"Interfaz {nombre_interfaz} configurada en modo access con VLAN {vlan}.")
                                break
                            else:
                                print("Número de VLAN inválido. Debe estar entre 1 y 4094.")
                        except ValueError:
                            print("Ingrese un número válido o 'c' para cancelar.")
                elif opcion == '2':
                    vlans_permitidas = input("Ingrese las VLANs permitidas (separadas por comas, o 'all' para todas): ")
                    if vlans_permitidas.lower() != 'all':
                        vlans_permitidas = [int(vlan) for vlan in vlans_permitidas.split(",") if vlan.strip()]

                    dispositivo.configuracion[nombre_interfaz] = {
                        "switchport mode": "trunk",
                        "switchport trunk allowed vlan": vlans_permitidas if vlans_permitidas else 'all'
                    }
                    self.datos_actuales.guardar_datos()
                    print(f"Interfaz {nombre_interfaz} configurada en modo trunk.")
                elif opcion == '3':
                    break
                else:
                    print("Opción inválida.")

    def configurar_servicios(self, dispositivo):
        servicios = ["OSPF", "RIPv2", "BGP"]
        while True:
            print("\n--- Configuración de Servicios ---")
            for i, servicio in enumerate(servicios):
                print(f"{i+1}. {servicio}")
            print(f"{len(servicios)+1}. Salir")

            try:
                opcion = int(input("Seleccione un servicio: ")) - 1
                if 0 <= opcion < len(servicios):
                    servicio_seleccionado = servicios[opcion]
                    self.configurar_servicio(dispositivo, servicio_seleccionado)  
                elif opcion == len(servicios):
                    break
                else:
                    raise ValueError("Opción inválida.")
            except ValueError:
                print("Ingrese un número válido.")
                
    def configurar_servicio(self, dispositivo, servicio):
        if servicio == "OSPF":
            process_id = input("Ingrese el ID del proceso OSPF: ")
            router_id = input("Ingrese el Router ID: ")
            while True:
                network = input("Ingrese la red (formato x.x.x.x): ")
                if validar_ip(network):
                    break
                else:
                    print("Dirección IP inválida. Intente de nuevo.")
            while True:
                mask = input("Ingrese la máscara de red (formato x.x.x.x): ")
                if validar_mascara_red(mask):
                    break
                else:
                    print("Máscara de red inválida. Intente de nuevo.")
            area = input("Ingrese el área: ")
            dispositivo.configuracion["router ospf " + process_id] = {
                "router-id": router_id,
                "network": f"{network} {mask} area {area}"
            }
        elif servicio == "RIPv2":
            while True:
                network = input("Ingrese la red (formato x.x.x.x): ")
                if validar_ip(network):
                    break
                else:
                    print("Dirección IP inválida. Intente de nuevo.")
            while True:
                mask = input("Ingrese la máscara de red (formato x.x.x.x): ")
                if validar_mascara_red(mask):
                    break
                else:
                    print("Máscara de red inválida. Intente de nuevo.")
            dispositivo.configuracion["router rip"] = {
                "version": 2,
                "network": network,
                "mask": mask
            }
        elif servicio == "BGP":
            local_as = input("Ingrese el AS local: ")
            while True:
                neighbor = input("Ingrese la dirección IP del vecino BGP: ")
                if validar_ip(neighbor):
                    break
                else:
                    print("Dirección IP inválida. Intente de nuevo.")
            remote_as = input("Ingrese el AS remoto: ")
            dispositivo.configuracion[f"router bgp {local_as}"] = {
                "neighbor": neighbor,
                "remote-as": remote_as
            }

        self.datos_actuales.guardar_datos()
        print(f"Servicio {servicio} configurado exitosamente.")
from cryptography.fernet import Fernet
from datetime import datetime
import json
import base64
import os
import hashlib


class Chozita:
    """
    FernetConCoca Biblioteca para cifrar y descifrar archivos utilizando Fernet y guardar los datos en formato JSON.
    """

    def __init__(self):
        pass

    def _password(self, Password):
        """
        Genera una clave de cifrado a partir de una contraseña utilizando SHA-256 y base64.

        Parámetros:
        - Password: Contraseña para generar la clave de cifrado.

        Retorna:
        - Clave de cifrado generada.
        """
        return base64.urlsafe_b64encode(hashlib.sha256(Password.encode()).digest()[:32])

    def cifrar(self, archivo_path: str, password: str, comentario: str = None) -> tuple[bool, str]:
        """
        Cifra el contenido de un archivo y guarda el contenido cifrado en un JSON.

        Args:
            archivo_path (str): La ruta del archivo que deseas cifrar.
            password (str): Contraseña para cifrar el contenido.
            comentario (str): Comentario adicional para dejar en el JSON.

        Returns:
            tuple[bool, str]:
                bool: True si el cifrado fue correcto, False en caso contrario.
                str: Mensaje de error en caso de que bool sea False; de lo contrario, una cadena vacía.
        """
        try:
            # Abrir el archivo a cifrar
            with open(archivo_path, 'rb') as file:
                datos = file.read()
                # pasar los datos a 64
                datos64 = base64.b64encode(datos).decode('utf-8')

                # crear la instancia fernet
                instancia_fernet = Fernet(self._password(password))

                # cifrar los datos (datos64)
                datos_cifrados = instancia_fernet.encrypt(
                    datos64.encode()).decode('utf-8')

                # Verificar si hay un '/' en la ruta para el manejo del path
                if os.path.dirname(archivo_path) != '':
                    # Lectura del path para extrar datos nesesarios
                    path_archivo, nombre_archivo = os.path.split(archivo_path)
                    datos_nombre, datos_extensio = os.path.splitext(
                        nombre_archivo)

                    # construccion del path final
                    path = os.path.join(path_archivo, datos_nombre, + '.json')
                else:
                    datos_nombre, datos_extensio = os.path.splitext(
                        archivo_path)
                    # construccion del path final
                    path = os.path.join(os.getcwd(), datos_nombre + '.json')

                # Preparar los datos para guardar en el archivo JSON
                datos_paquete = {
                    "Nombre": datos_nombre,
                    "Extension": datos_extensio,
                    "Anotacion": comentario,
                    "Contenido": datos_cifrados
                }

                # Escribir los datos cifrados en el archivo JSON
                with open(path, 'w') as archivo:
                    json.dump(datos_paquete, archivo, indent=4)
                    return [True, '']
        except Exception as Error:
            return [False, str(Error)]

    def descifrar(self, json_path: str, password: str) -> tuple[bool, str]:
        """
        Descifra el contenido de un archivo JSON cifrado y guarda el archivo descifrado.

        Args:
            json_path (str): La ruta del archivo JSON que contiene el contenido cifrado.
            password (str): Contraseña para descifrar el contenido cifrado.

        Returns:
            tuple[bool, str]:
                bool: True si el descifrado fue correcto, False en caso contrario.
                str: Mensaje de error en caso de que bool sea False, de lo contrario una cadena vacía.
        """
        try:
            # Cargar el JSON con el contenido cifrado
            with open(json_path, 'rb') as contenido_json:
                datos_json = json.load(contenido_json)

                # Verificar si hay un '/' en la ruta para el manejo del path
                if os.path.dirname(json_path) != '':
                    # Usar el path del archivo si el archivo tiene una ruta extensa
                    # Ejemplo: src/img.png
                    directorio_final = os.path.dirname(json_path)
                else:
                    # Usar el path actual si la ruta no es extensa
                    # Ejemplo: img.png
                    directorio_final = os.getcwd()

                # Cargar nombre y extensión del archivo descifrado
                archivo_path = os.path.join(
                    directorio_final, datos_json['Nombre'] +
                    datos_json['Extension']
                )

                # Crear la instancia Fernet para descifrar el contenido
                instancia_fernet = Fernet(self._password(password))

                # Descifrar el contenido usando la instancia Fernet
                contenido = datos_json['Contenido']
                contenido = instancia_fernet.decrypt(contenido.encode())

                # Decodificar el contenido de base64
                contenido = base64.b64decode(contenido)
                
                # Crear el archivo descifrado
                with open(archivo_path, 'wb') as archivo:
                    archivo.write(contenido)
                    return [True, ""]
        except Exception as Error:
            return [False, str(Error)]

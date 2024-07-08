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

    def Cifrar(self, Objetivo, Password, Anotacion=None, User=None):
        """
        Cifra el contenido de un archivo y guarda los datos en un archivo JSON.

        Parámetros:
        - Objetivo: Ruta del archivo a cifrar.
        - Password: Contraseña para el cifrado.
        - Anotación: Comentario sobre el archivo (Opcional).
        - Usuario: Nombre del usuario (Opcional).

        Guarda el archivo cifrado como `NombreArchivo.json`.
        """
        with open(Objetivo, 'rb') as ArchivoObjetivo:
            DatosArchivo = ArchivoObjetivo.read()
            Datos64 = base64.b64encode(DatosArchivo).decode('utf-8')

            ObjetoFernet = Fernet(self._password(Password))
            ContenidoCifrado = ObjetoFernet.encrypt(
                Datos64.encode()).decode('utf-8')
            if os.path.dirname(Objetivo) != '':
                Directorio, NombreArchivo = os.path.split(Objetivo)
                Nombre, Extension = os.path.splitext(NombreArchivo)
                PATH = Directorio + '/' + Nombre + ".json"
            else:
                Nombre, Extension = os.path.splitext(Objetivo)
                PATH = Nombre + '.json'
            FechaActual = datetime.now()
            FechaFormateada = FechaActual.strftime("%Y-%m-%d %H:%M:%S")

            DatosJson = {
                "Nombre": Nombre,
                "Extension": Extension,
                "Fecha": FechaFormateada,
                "Anotacion": Anotacion,
                "User": User,
                "Contenido": ContenidoCifrado
            }

            with open(PATH, 'w') as ArchivoCifrado:
                json.dump(DatosJson, ArchivoCifrado, indent=4)

    def descifrar_json(self, json_path: str, password: str) -> tuple[bool, str]:
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
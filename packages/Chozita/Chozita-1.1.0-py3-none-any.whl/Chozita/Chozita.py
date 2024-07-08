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

    def _Password(self, Password):
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

            ObjetoFernet = Fernet(self._Password(Password))
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

    def Descifrar(self, Objetivo, Password):
        """
        Descifra el contenido de un archivo cifrado y guarda el archivo descifrado.

        Parámetros:
        - Objetivo: Ruta del archivo JSON cifrado.
        - Password: Contraseña para el descifrado.
        """
        with open(Objetivo, 'rb') as ArchivoObjetivo:
            ConjuntoDatos = json.load(ArchivoObjetivo)
            if os.path.dirname(Objetivo) != '':
                Directorio = os.path.dirname(Objetivo)
            else:
                Directorio = os.getcwd()
            PathArchivoResultado = os.path.join(
                Directorio, ConjuntoDatos['Nombre'] + ConjuntoDatos['Extension'])
            ObjetoFernet = Fernet(self._Password(Password))
            ContenidoCifrado = ConjuntoDatos['Contenido']
            ContenidoDescifrado = ObjetoFernet.decrypt(
                ContenidoCifrado.encode())

            Contenido = base64.b64decode(ContenidoDescifrado)

            with open(PathArchivoResultado, 'wb') as ArchivoDescifrado:
                ArchivoDescifrado.write(Contenido)

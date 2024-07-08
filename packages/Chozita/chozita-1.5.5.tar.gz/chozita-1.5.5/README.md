# Chozita 

Chozita es una mini librería para encriptar y desencriptar archivos utilizando Fernet como intermediario.

![Imagen de GitHub](github/wallgit.jpg)

![License](https://img.shields.io/badge/license-MIT-green) ![Version](https://img.shields.io/badge/version-1.4.1-green) ![Python](https://img.shields.io/badge/python-green?logo=python) ![Fernet](https://img.shields.io/badge/fernet-encryption-green?logo=shield&style=flat)

### Objetivo de Chozita
El objetivo de Chozita es simplificar el proceso de encriptar archivos para marcos de trabajo como Tkinter.

### Estado Actual
Actualmente, cuenta con dos funciones básicas para trabajar (`cifrar` y `descifrar`). Estas son las implementaciones iniciales de la librería. En futuras versiones, se añadirán más métodos, como la capacidad de distribuir el contenido cifrado en múltiples archivos JSON en lugar de uno solo, y la implementación de compresión ZIP.

#### Instalación
```bash
pip install Chozita
```

#### Explicación de la idea para la implementación con ZIP
El cifrado se realizará como en el formato actual, pero el contenido estará distribuido en múltiples archivos dentro de un archivo ZIP. La función se encargará directamente de descomprimir y leer los archivos internos para descifrarlos y recrear el contenido original.

### Notas
La biblioteca maneja automáticamente los `PATH`. Si se indica cifrar un archivo, por ejemplo: `src/img.jpg`, el archivo JSON que contiene los datos cifrados se creará automáticamente en el mismo `PATH` con el nombre `src/img.json`. Lo mismo ocurre para ambas funciones de cifrado.

### Ejemplo de código
Las funciones devuelven una tupla de datos `[bool, string]`:
- `bool` devuelve `True` si se ejecutó correctamente y `False` si hubo algún error.
- `string` permanece vacío si todo funciona correctamente, pero contiene el mensaje de error si `bool` es `False`.

```python
from Chozita import Chozita

# Crear la instancia
C = Chozita()

# Ejemplo de cifrado y descifrado
CheckValue, ErrorString = C.cifrar('img.jpg', 'password')
if not CheckValue:
    print(ErrorString)

CheckValue, ErrorString = C.descifrar('img.json', 'password')
if not CheckValue:
    print(ErrorString)

# Ejemplo utilizando rutas específicas
CheckValue, ErrorString = C.cifrar('src/img.jpg', 'password')
if not CheckValue:
    print(ErrorString)

CheckValue, ErrorString = C.descifrar('src/img.json', 'password')
if not CheckValue:
    print(ErrorString)
```
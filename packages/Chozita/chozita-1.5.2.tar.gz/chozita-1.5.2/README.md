# Chozita 

Chozita es una mini librería para `encriptar` y `desencriptar` archivos utilizando `Fernet` como intermediario.

![Imagen de GitHub](github/wallgit.jpg)

![License](https://img.shields.io/badge/license-MIT-green) ![Version](https://img.shields.io/badge/version-1.4.1-green) ![Python](https://img.shields.io/badge/python-green?logo=python) ![Fernet](https://img.shields.io/badge/fernet-encryption-green?logo=shield&style=flat)

### Objetivo de Chozita
> El objetivo de Chozita es simplificar el proceso de encriptar archivos para marcos de trabajo como `Tkinter`.

### Estado Actual
Actualmente, cuenta con dos funciones básicas para trabajar (`cifrar` y `descifrar`). Estas son las implementaciones iniciales de la librería, pero en el futuro se añadirán más métodos, como la capacidad de repartir el contenido cifrado en varios archivos JSON en lugar de uno solo, y la implementación de compresión ZIP 

#### Explicacion de mi idea para la implemtacion zip
> Cifrar el contenido en el formato actual, pero el contenido ira repartido en multiples archivos pero se utilizara un zip y la funcion se encargara directamente de descomprimir y leer los archivos internos para descifrarlos y recrear el contenido original

from setuptools import setup, find_packages

# Leer el contenido del README.md para usarlo como long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='Chozita',
    version='1.5.2',
    author='baaaaa',
    author_email='devbaats@gmail.com',
    description='Una mini librería de automatización de cifrado de archivos',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BAA4TS/Chozita',
    packages=find_packages(),  # Encuentra automáticamente los paquetes
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    keywords=['Cifrado', 'Python', 'Fernet', 'Automatización'],
    license='MIT',
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'cryptography>=3.0',
    ],
)

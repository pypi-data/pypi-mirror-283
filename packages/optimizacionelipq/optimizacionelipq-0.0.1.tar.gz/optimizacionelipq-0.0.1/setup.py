from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Métodos de optimización'
LONG_DESCRIPTION = 'Paquete de Python para compartir los algoritmos de optimización univariable y multivariable y funciones objetivo que se desarrollen en clase.'

# Configurando
setup(
    # El nombre debe coincidir con el nombre de la carpeta principal
    name="optimizacionelipq", 
    version=VERSION,
    author="Eli",
    author_email="tuemail@email.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',  # Ensure proper rendering on PyPI
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    keywords=['Python', 'optimización', 'funciones', 'gráficas'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify minimum Python version
)

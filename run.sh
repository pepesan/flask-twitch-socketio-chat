#!/bin/bash
source /path/to/venv/bin/activate   # Activa el entorno virtual
export FLASK_APP=app.py             # Indica el archivo que contiene la aplicación Flask
export FLASK_ENV=development       # Establece el modo de desarrollo (opcional)
flask run                           # Ejecuta el servidor Flask

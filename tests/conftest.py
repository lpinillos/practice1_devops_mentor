"""
Configuración común para todas las pruebas.

pytest importa este archivo ANTES que los módulos de test, así que es el lugar
correcto para preparar el entorno antes de que se importe `app.py`.

Reto resuelto aquí: app.py, al importarse, intenta crear y escribir en
/mnt/logs/app.log (ver app.py líneas 11-12). En una máquina de pruebas esa ruta
no existe. Redirigimos LOG_PATH a un archivo temporal ANTES de importar la app.
"""
import os
import tempfile

# Debe ejecutarse antes de cualquier "import app" -> por eso va aquí arriba.
os.environ["LOG_PATH"] = os.path.join(tempfile.gettempdir(), "devops-mentor-test.log")

import pytest
from app import app as flask_app


@pytest.fixture
def client():
    """
    Cliente de pruebas de Flask: permite enviar peticiones HTTP simuladas
    (GET/POST) a la app SIN levantar un servidor real ni abrir un puerto.
    """
    flask_app.config.update({"TESTING": True})
    with flask_app.test_client() as c:
        yield c

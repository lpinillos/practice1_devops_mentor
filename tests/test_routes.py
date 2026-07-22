"""
Pruebas de INTEGRACIÓN de las rutas Flask.

Usamos el `client` (fixture definido en conftest.py) para simular peticiones
HTTP reales. En /upload usamos "mocking" para NO llamar a Azure de verdad.
"""
import io
from unittest.mock import patch, MagicMock


# ── Ruta "/" (calculadora) ──────────────────────────────────────────────────
class TestIndex:
    def test_get_devuelve_formulario(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        # La página debe contener el formulario de la calculadora.
        assert "Calculadora".encode() in resp.data or b"Calcular" in resp.data

    def test_post_valido_muestra_resultado(self, client):
        resp = client.post("/", data={
            "peso": "70", "altura": "175", "edad": "25",
            "sexo": "masculino", "actividad": "moderado",
        })
        assert resp.status_code == 200
        # Debe aparecer el IMC calculado (22.86) en la respuesta.
        assert b"22.86" in resp.data

    def test_post_valores_negativos_muestra_error(self, client):
        resp = client.post("/", data={
            "peso": "-70", "altura": "175", "edad": "25",
            "sexo": "masculino", "actividad": "moderado",
        })
        assert resp.status_code == 200
        # El mensaje de error de la app menciona "positivos".
        assert "positivos".encode() in resp.data


# ── Ruta "/upload" (subida a Blob Storage) ──────────────────────────────────
class TestUpload:
    def test_sin_archivo_devuelve_400(self, client):
        resp = client.post("/upload")
        assert resp.status_code == 400
        assert "No se adjunt" in resp.get_json()["error"]

    def test_extension_invalida_devuelve_400(self, client):
        data = {"imagen": (io.BytesIO(b"contenido falso"), "documento.txt")}
        resp = client.post("/upload", data=data, content_type="multipart/form-data")
        assert resp.status_code == 400
        assert "inv" in resp.get_json()["error"].lower()  # "inválido"

    @patch("app.BlobServiceClient")
    def test_subida_exitosa_con_mock(self, mock_blob_service, client):
        """
        Reemplazamos BlobServiceClient por un objeto falso: la app cree que
        habló con Azure, pero en realidad nunca sale a la red.
        """
        blob_falso = MagicMock()
        blob_falso.url = "https://fake.blob.core.windows.net/imagenes/x.png"
        (mock_blob_service.from_connection_string
            .return_value.get_container_client
            .return_value.get_blob_client
            .return_value) = blob_falso

        data = {"imagen": (io.BytesIO(b"\x89PNG bytes falsos"), "foto.png")}
        resp = client.post("/upload", data=data, content_type="multipart/form-data")

        assert resp.status_code == 200
        body = resp.get_json()
        assert body["mensaje"] == "Imagen subida correctamente"
        assert body["blob"].endswith(".png")
        # Verificamos que la app INTENTÓ subir el blob exactamente una vez.
        blob_falso.upload_blob.assert_called_once()

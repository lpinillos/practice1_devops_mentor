import os
import uuid
import logging
from flask import Flask, render_template, request, jsonify
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Logging ──────────────────────────────────
LOG_PATH = os.environ.get("LOG_PATH", "/mnt/logs/app.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)



# Blob Storage ──────────────────────────────────────────────────────────────
CONN_STR        = os.environ.get("AZURE_STORAGE_CONNECTION_STRING", "")
BLOB_CONTAINER  = os.environ.get("BLOB_CONTAINER_NAME", "imagenes")

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

# Lógica de negocio ─────────────────────────────────────────────────────────
def calcular_imc(peso_kg, altura_m):
    imc = peso_kg / (altura_m ** 2)
    if imc < 18.5:
        categoria = "Bajo peso"
    elif imc < 25:
        categoria = "Peso normal"
    elif imc < 30:
        categoria = "Sobrepeso"
    else:
        categoria = "Obesidad"
    return round(imc, 2), categoria

def calcular_tmb(peso_kg, altura_cm, edad, sexo, actividad):
    if sexo == "masculino":
        tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * edad) + 5
    else:
        tmb = (10 * peso_kg) + (6.25 * altura_cm) - (5 * edad) - 161

    factores = {
        "sedentario": 1.2, "ligero": 1.375,
        "moderado": 1.55, "activo": 1.725, "muy_activo": 1.9
    }
    calorias = tmb * factores.get(actividad, 1.2)
    return round(calorias, 2), round(tmb, 2)

# ── Rutas ─────────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    resultado, error = None, None
    if request.method == "POST":
        try:
            peso   = float(request.form["peso"])
            altura = float(request.form["altura"])
            edad   = int(request.form["edad"])
            sexo   = request.form["sexo"]
            activ  = request.form["actividad"]
            if peso <= 0 or altura <= 0 or edad <= 0:
                raise ValueError("Los valores deben ser positivos.")
            altura_m = altura / 100
            imc, categoria = calcular_imc(peso, altura_m)
            calorias, tmb  = calcular_tmb(peso, altura, edad, sexo, activ)
            resultado = {
                "imc": imc, "categoria": categoria,
                "calorias": calorias, "tmb": tmb,
                "peso": peso, "altura": altura, "edad": edad,
                "emoji": "⚠️" if imc < 18.5 or imc >= 30 else "✅"
            }
            logger.info(f"Cálculo IMC: peso={peso} altura={altura} imc={imc} cat={categoria}")
        except ValueError as e:
            error = str(e)
            logger.warning(f"Error en formulario: {e}")
    return render_template("index.html", resultado=resultado, error=error)


@app.route("/upload", methods=["POST"])
def upload_imagen():
    if "imagen" not in request.files:
        return jsonify({"error": "No se adjuntó ninguna imagen"}), 400
    archivo = request.files["imagen"]
    if archivo.filename == "" or not allowed_file(archivo.filename):
        return jsonify({"error": "Archivo inválido. Solo se permiten: png, jpg, jpeg, gif, webp"}), 400
    try:
        ext       = archivo.filename.rsplit(".", 1)[1].lower()
        blob_name = f"{uuid.uuid4()}.{ext}"
        client    = BlobServiceClient.from_connection_string(CONN_STR)
        blob      = client.get_container_client(BLOB_CONTAINER).get_blob_client(blob_name)
        blob.upload_blob(archivo.read())
        logger.info(f"Imagen subida al blob: {blob_name}")
        return jsonify({"mensaje": "Imagen subida correctamente", "blob": blob_name, "url": blob.url})
    except Exception as e:
        logger.error(f"Error subiendo imagen: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
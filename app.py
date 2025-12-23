import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from utils.face_utils import register_face, recognize_face
from utils.upload_utils import save_uploaded_files

app = Flask(__name__)
CORS(app)

# Configuração do Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "faces"
VECTOR_SIZE = 128  # Tamanho do embedding do face_recognition

qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def init_qdrant():
    """Inicializa a collection do Qdrant se não existir."""
    collections = qdrant.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{COLLECTION_NAME}' criada com sucesso.")


@app.route("/post-face", methods=["POST"])
def post_face():
    """Rota para cadastrar rosto."""
    label = request.form.get("label")
    if not label:
        return jsonify({"error": "O campo 'label' é obrigatório."}), 400

    files = save_uploaded_files(request.files, "uploads/")
    if len(files) < 3:
        return jsonify({"error": "Por favor, envie 3 imagens para o cadastro."}), 400

    result = register_face(files, label, qdrant)
    if result:
        return jsonify({"message": "Rosto cadastrado com sucesso."})
    return jsonify({"error": "Erro ao registrar o rosto."}), 500


@app.route("/check-face", methods=["POST"])
def check_face():
    """Rota para reconhecer rosto."""
    if "File1" not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada."}), 400

    file_path = save_uploaded_files(request.files, "uploads/", single=True)
    results = recognize_face(file_path, qdrant)

    if not results:
        return jsonify({"message": "Nenhuma correspondência encontrada."})

    return jsonify({"result": results})


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    init_qdrant()
    app.run(debug=True, host="0.0.0.0", port=5001)

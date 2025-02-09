from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from utils.face_utils import register_face, recognize_face
from utils.upload_utils import save_uploaded_files

app = Flask(__name__)
CORS(app)

# Configuração do MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/facial_recognition"
mongo = PyMongo(app)

# Rota para cadastrar rosto
@app.route("/post-face", methods=["POST"])
def post_face():
    label = request.form.get("label")
    if not label:
        return jsonify({"error": "O campo 'label' é obrigatório."}), 400

    # Salvar os arquivos enviados
    files = save_uploaded_files(request.files, "uploads/")
    if len(files) < 3:
        return jsonify({"error": "Por favor, envie 3 imagens para o cadastro."}), 400

    # Registrar o rosto
    result = register_face(files, label, mongo)
    if result:
        return jsonify({"message": "Rosto cadastrado com sucesso."})
    return jsonify({"error": "Erro ao registrar o rosto."}), 500


# Rota para reconhecer rosto
@app.route("/check-face", methods=["POST"])
def check_face():
    if "File1" not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada."}), 400

    file_path = save_uploaded_files(request.files, "uploads/", single=True)
    results = recognize_face(file_path, mongo)
    if not results:
        return jsonify({"message": "Nenhuma correspondência encontrada."})
    print(results)
    return jsonify({"result": results})


if __name__ == "__main__":
    app.run(debug=True, port=5001)

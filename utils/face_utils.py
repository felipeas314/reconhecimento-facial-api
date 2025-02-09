import face_recognition
import numpy as np
from models.embeddings import save_embedding, load_embeddings


def register_face(image_paths, label, mongo):
    try:
        embeddings = []
        for path in image_paths:
            image = face_recognition.load_image_file(path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                embeddings.append(face_encodings[0])
        if embeddings:
            save_embedding(label, embeddings, mongo)
            return True
    except Exception as e:
        print(f"Erro ao registrar rosto: {e}")
    return False


def recognize_face(image_path, mongo):
    try:
        # Carregar a imagem
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if not face_encodings:
            return []

        # Carregar embeddings do banco de dados
        embeddings = load_embeddings(mongo)

        results = []
        for encoding in face_encodings:
            distances = []
            labels = []
            for face in embeddings:
                for descriptor in face["descriptors"]:
                    distance = np.linalg.norm(encoding - np.array(descriptor))
                    distances.append(distance)
                    labels.append(face["label"])
            # Encontrar a menor distância
            min_distance_index = np.argmin(distances)
            if distances[min_distance_index] < 0.6:
                results.append({"label": labels[min_distance_index], "distance": distances[min_distance_index]})
        return results
    except Exception as e:
        print(f"Erro ao reconhecer rosto: {e}")
    return []

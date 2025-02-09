from flask_pymongo import PyMongo

def save_embedding(label, embeddings, mongo: PyMongo):
    face_data = {
        "label": label,
        "descriptors": [embedding.tolist() for embedding in embeddings],
    }
    mongo.db.faces.insert_one(face_data)


def load_embeddings(mongo: PyMongo):
    faces = mongo.db.faces.find()
    embeddings = []
    for face in faces:
        descriptors = [list(d) for d in face["descriptors"]]
        embeddings.append({"label": face["label"], "descriptors": descriptors})
    return embeddings

# backend/embeddings.py
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image as keras_image

# load model once
MODEL = ResNet50(weights="imagenet", include_top=False, pooling="avg")

def get_embedding(file_path: str):
    """Return L2-normalized embedding (numpy array) for an image file."""
    img = keras_image.load_img(file_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    emb = MODEL.predict(x, verbose=0).flatten()
    norm = np.linalg.norm(emb)
    if norm == 0:
        return emb
    return emb / norm


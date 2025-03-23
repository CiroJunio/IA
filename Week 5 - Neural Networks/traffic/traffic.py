import os
import sys
import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# Constantes
EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43  # Atualizado para refletir um dataset comum de sinais de trânsito
TEST_SIZE = 0.4

def main():
    """Função principal para treinar e, opcionalmente, salvar o modelo."""
    if len(sys.argv) not in [2, 3]:
        sys.exit("Uso: python traffic.py pasta_dados [modelo.h5]")

    data_dir = sys.argv[1]
    images, labels = load_data(data_dir)

    # Pré-processar os dados
    labels = tf.keras.utils.to_categorical(labels, NUM_CATEGORIES)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Construir e treinar o modelo
    model = get_model()
    model.fit(x_train, y_train, epochs=EPOCHS, validation_data=(x_test, y_test))

    # Avaliar o modelo
    loss, accuracy = model.evaluate(x_test, y_test, verbose=2)
    print(f"Acurácia no teste: {accuracy * 100:.2f}%")

    # Salvar o modelo se o nome do arquivo for fornecido
    if len(sys.argv) == 3:
        model.save(sys.argv[2])
        print(f"Modelo salvo em {sys.argv[2]}.")

def load_data(data_dir):
    """Carregar imagens e rótulos do diretório do dataset."""
    images, labels = [], []
    for category in range(NUM_CATEGORIES):
        category_path = os.path.join(data_dir, str(category))
        if not os.path.exists(category_path):
            continue
        for filename in os.listdir(category_path):
            img_path = os.path.join(category_path, filename)
            image = cv2.imread(img_path)
            if image is not None:
                image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT)) / 255.0  # Normalização
                images.append(image)
                labels.append(category)
    return images, labels

def get_model():
    """Construir e compilar a rede neural convolucional."""
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

if __name__ == "__main__":
    main()
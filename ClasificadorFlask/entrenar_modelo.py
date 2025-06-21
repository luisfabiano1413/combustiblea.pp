from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical

# 1. Cargar datos MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 2. Normalizar
x_train = x_train / 255.0
x_test = x_test / 255.0

# 3. Codificar las etiquetas (one-hot)
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# 4. Definir el modelo
modelo = Sequential([
    Flatten(input_shape=(28, 28)),     # Aplana la imagen 28x28
    Dense(128, activation='relu'),     # Capa oculta
    Dense(10, activation='softmax')    # Capa de salida (10 clases)
])

# 5. Compilar
modelo.compile(optimizer='adam',
               loss='categorical_crossentropy',
               metrics=['accuracy'])

# 6. Entrenar
modelo.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# 7. Guardar el modelo entrenado
modelo.save('model.h5')

print("✅ Modelo entrenado y guardado como model.h5")

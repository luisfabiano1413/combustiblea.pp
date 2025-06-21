import os
import numpy as np
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

# Configuración inicial
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Base de datos
db = SQLAlchemy(app)

class Imagen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    prediccion = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

# Modelo de IA
modelo = MobileNetV2(weights='imagenet')
print("Modelo MobileNetV2 cargado correctamente")

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        archivo = request.files.get('imagen')
        if archivo:
            nombre_seguro = secure_filename(archivo.filename)
            ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro)
            archivo.save(ruta)

            # Procesar imagen
            img = image.load_img(ruta, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            predicciones = modelo.predict(img_array)
            decoded = decode_predictions(predicciones, top=1)[0][0]  # top 1

            clase = decoded[1]  # nombre de clase (ej: 'guitar', 'cat')
            probabilidad = float(decoded[2]) * 100  # porcentaje

            resultado = f"{clase.upper()} ({probabilidad:.2f}%)"

            nueva_img = Imagen(filename=nombre_seguro, prediccion=resultado)
            db.session.add(nueva_img)
            db.session.commit()

    imagenes = Imagen.query.order_by(Imagen.id.desc()).limit(5).all()
    return render_template('index.html', resultado=resultado, imagenes=imagenes)

if __name__ == '__main__':
    app.run(debug=True)

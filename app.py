
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import json

app = Flask(__name__)

# Load trained AI model
model = load_model("plant_disease_model.keras")

# Load plant disease names
with open("class_names.json", "r") as f:
    class_names = json.load(f)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Predict plant disease
@app.route("/predict", methods=["POST"])
def predict():

    file = request.files.get("file")

    if not file or file.filename == "":
        return render_template(
            "index.html",
            error="Please select a plant image.",
            prediction=None,
            confidence=None,
            uploaded_image=None
        )

    try:
        # Open uploaded image
        image = Image.open(file).convert("RGB")

        # Resize image
        image = image.resize((160, 160))

        # Convert image into array
        image_array = np.array(image) / 255.0

        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)

        # Predict disease
        result = model.predict(image_array, verbose=0)

        # Get predicted class
        class_index = int(np.argmax(result[0]))

        disease = class_names[class_index]

        # Calculate confidence
        confidence = float(result[0][class_index]) * 100

        # Display result
        return render_template(
            "index.html",
            prediction=disease,
            confidence=f"{confidence:.2f}%",
            uploaded_image=None
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Unable to predict: {e}",
            prediction=None,
            confidence=None,
            uploaded_image=None
        )


# Run application
if __name__ == "__main__":
    app.run(debug=True)

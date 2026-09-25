from flask import Flask, request, jsonify
import util
from flask_cors import CORS

app = Flask(__name__)
app.config['MAX_FORM_MEMORY_SIZE'] = 10 * 1024 * 1024 
CORS(app)

util.load_saved_artifacts()


@app.route('/classify_image', methods=['GET', 'POST'])
def classify_image():
    if 'image_data' not in request.form:
        return jsonify({"error": "Missing field: image_data"}), 400

    image_data = request.form['image_data']

    try:
        result = util.classify_image(image_data, None)
    except Exception:
        return jsonify({"error": "Could not process image_data"}), 400

    return jsonify(result)

if __name__ == "__main__":
     print("Starting Python Flask Server For Sports Celebrity Image Classification")
     app.run(port=5000)
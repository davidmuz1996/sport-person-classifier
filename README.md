# Sport Person Classifier

A sports celebrity image classifier: upload a photo and it identifies which of five athletes is in it, using OpenCV face/eye detection, a wavelet-transform feature pipeline, and a scikit-learn classifier served through a Flask API.

**Supported classes:** Lionel Messi, Maria Sharapova, Roger Federer, Serena Williams, Virat Kohli.

## How it works

1. The frontend (`UI/`) lets you drag-and-drop or upload an image.
2. The image is sent as base64 to the Flask API (`server/`).
3. OpenCV's Haar cascades detect a face and require **at least two eyes** to be found in it — this filters out non-frontal/low-quality crops. If no valid face is found, the API returns an empty result.
4. Each detected face is resized and combined with a wavelet-transformed version of itself (via `PyWavelets`) into a single feature vector.
5. A pre-trained scikit-learn classifier (`server/artifacts/saved_model.pkl`) predicts the class and a probability score per class.

```
Browser --> nginx --> static UI files
              |
              +--> /classify_image --> gunicorn --> Flask app --> OpenCV + scikit-learn model
```

## Project structure

```
server/           Flask API, face/eye detection, feature pipeline, trained model
  server.py       API entry point (POST /classify_image)
  util.py         Image processing + classification logic
  wavelet.py       Wavelet transform helper
  artifacts/       Trained model + class-to-label mapping
  haarcascades/     OpenCV face/eye detection cascades
UI/               Static frontend (HTML/CSS/JS, Dropzone.js for uploads)
model/            Jupyter notebook covering data collection, feature engineering, and model training
```

## Running it locally

**Backend:**

```bash
cd server
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

The API starts on `http://localhost:5000`.

**Frontend:** open `UI/app.html` directly in a browser, or serve the folder with any static file server, e.g.:

```bash
cd UI
python3 -m http.server 8080
```

Then open `http://localhost:8080/app.html`. Note: `app.js` currently points at a relative `/classify_image` path for the deployed (nginx-proxied) setup — for local testing against the Flask dev server directly, point it at `http://localhost:5000/classify_image` instead.

## API

**`POST /classify_image`**

Form-encoded body with one field:

| Field | Type | Description |
| --- | --- | --- |
| `image_data` | string | Base64-encoded image, e.g. `data:image/jpeg;base64,...` |

Response — a list with one entry per detected face:

```json
[
  {
    "class": "maria_sharapova",
    "class_probability": [3.87, 4.0, 1.23, 3.87, 87.65],
    "class_dictionary": {
      "roger_federer": 0,
      "serena_williams": 1,
      "virat_kohli": 2,
      "lionel_messi": 3,
      "maria_sharapova": 4
    }
  }
]
```

An empty list `[]` means no face with two clearly detectable eyes was found in the image.

## Deployment

Deployed on an AWS EC2 instance running Ubuntu, with:
- **gunicorn** as the production WSGI server for the Flask API
- **systemd** to keep it running permanently and restart on crash
- **nginx** serving the static frontend and reverse-proxying `/classify_image` to gunicorn

## Notes

- `model/dataset/` and `model/cropped_data/` (the training images) are intentionally excluded from this repository — see `.gitignore`.

## Credits

Based on the "Sports Celebrity Image Classification" project by [codebasics](https://codebasics.io) (Dhaval Patel) — original tutorial, project structure, and approach. This repository is my own implementation, extended with a production deployment (nginx + gunicorn + systemd on AWS EC2).

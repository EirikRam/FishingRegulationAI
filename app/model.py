import cv2
import numpy as np
import requests
from tkinter import messagebox

def load_image(image_path, img_height, img_width):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (img_height, img_width))
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    return img


def predict_fish(image_path, prediction_key, prediction_endpoint, project_id, published_name):
    headers = {
        "Prediction-Key": prediction_key,
        "Content-Type": "application/octet-stream"
    }

    with open(image_path, "rb") as image_file:
        response = requests.post(
            f"{prediction_endpoint}/customvision/v3.0/Prediction/{project_id}/classify/iterations/{published_name}/image",
            headers=headers,
            data=image_file
        )

    if response.status_code != 200:
        messagebox.showerror("Error", "Request to Azure Custom Vision API failed.")
        return [], []

    response_json = response.json()
    if "predictions" not in response_json:
        messagebox.showerror("Error", "'predictions' key not found in the response.")
        return [], []

    predictions = response_json["predictions"]
    top_3 = sorted(predictions, key=lambda x: x["probability"], reverse=True)[:3]
    return [p["tagName"] for p in top_3], [p["probability"] for p in top_3]

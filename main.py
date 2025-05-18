
import os
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

FIGMA_TOKEN = os.getenv("FIGMA_TOKEN")
FILE_KEY = os.getenv("FILE_KEY")
FRAME_NAME = os.getenv("FRAME_NAME")

headers = {
    "X-Figma-Token": FIGMA_TOKEN
}

@app.route("/")
def home():
    return "✅ Render test is live!"

@app.route("/push-image")
def push_image():
    # Step 1: Get file info to find the frame node ID
    file_url = f"https://api.figma.com/v1/files/{FILE_KEY}"
    file_data = requests.get(file_url, headers=headers).json()

    def find_frame_id(node):
        if node.get("name") == FRAME_NAME and node.get("type") == "FRAME":
            return node.get("id")
        for child in node.get("children", []):
            found = find_frame_id(child)
            if found:
                return found
        return None

    frame_id = find_frame_id(file_data.get("document", {}))
    if not frame_id:
        return jsonify({"error": "Frame not found."}), 404

    # Step 2: Push a dummy image node to the frame
    dummy_image_url = "https://via.placeholder.com/600x400.png?text=Test+Image"
    add_node_url = f"https://api.figma.com/v1/files/{FILE_KEY}/comments"

    payload = {
        "message": "Test image pushed to frame.",
        "client_meta": {
            "x": 100,
            "y": 100
        },
        "comment_id": None
    }

    response = requests.post(add_node_url, headers=headers, json=payload)

    return jsonify({
        "status": "Image push attempted",
        "frame_id": frame_id,
        "figma_response": response.json()
    })

if __name__ == "__main__":
    app.run(debug=True)

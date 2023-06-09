# import cv2
# import numpy as np
# from flask import Flask, request, jsonify, send_file
# from PIL import Image
# import io


# app = Flask(__name__)

# @app.route('/process_image', methods=['POST'])
# def process_image():
#     # Get the uploaded image file
#     file = request.files['image']

#     # Load the image using PIL
#     pil_image = Image.open(io.BytesIO(file.read()))

#     # Convert the PIL image to OpenCV format
#     image = np.array(pil_image)
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Threshold the grayscale image to create a binary image
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

#     # Find the contours in the binary image
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     polygons = {}
#     # Create a mask for each polygon and save it to a separate file
#     for i, contour in enumerate(contours):
#         mask = np.zeros_like(gray)
#         cv2.drawContours(mask, [contour], 0, 255, -1)

#         # Save the x and y coordinates of each side of the contour to a dictionary
#         polygon_points = []
#         for point in contour:
#             x, y = point[0]
#             polygon_points.append([x, y])
#         polygons[f"polygon{i}"] = polygon_points

#     # Return the polygon dictionary as a JSON response
   
#     polygons = [[int(x), int(y)] for x, y, *_ in polygons]  # convert int32 to int and unpack only the first two values
#     return jsonify(polygons)
#     # return jsonify(polygons)

# if __name__ == '__main__':
#     app.run(debug=False)


# import cv2
# import numpy as np
# from flask import Flask, request, jsonify, send_file
# from PIL import Image
# import io
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route('/process_image', methods=['POST'])
# def process_image():
#     # Get the uploaded image file
#     file = request.files['image']
#     # Load the image using PIL
#     pil_image = Image.open(io.BytesIO(file.read()))

#     # Convert the PIL image to OpenCV format
#     image = np.array(pil_image)
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Threshold the grayscale image to create a binary image
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

#     # Find the contours in the binary image
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     polygons = {}
#     # Create a mask for each polygon and save it to a separate file
#     for i, contour in enumerate(contours):
#         mask = np.zeros_like(gray)
#         cv2.drawContours(mask, [contour], 0, 255, -1)

#         # Save the x and y coordinates of each side of the contour to a dictionary
#         polygon_points = []
#         for point in contour:
#             x, y = point[0]
#             polygon_points.append([x, y])
#         polygons[f"polygon{i}"] = polygon_points

#     # Return the polygon dictionary as a JSON response
#     polygons = {k: [[int(x), int(y)] for x, y in v] for k, v in polygons.items()}  # convert int32 to int
#     return jsonify(polygons)


# if __name__ == 'main':
#     app.run(debug=False)

from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route('/process_image', methods=['POST'])
# def get_polygons():
#     # Get the image file from the POST request
#     file = request.files['image']

#     # Read the image file using OpenCV
#     img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

#     # Convert image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Threshold image
#     ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

#     # Find contours of polygons
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     # Create a dictionary to store the polygons
#     polygons = {}

#     # Extract the x y coordinates for each polygon
#     for i, contour in enumerate(contours):

#         if i == 0 :
#             continue
#         # Get the x y coordinates of the current polygon
#         polygon = contour.squeeze().tolist()

#         # Add the polygon to the dictionary
#         polygons[f'polygon{i}'] = polygon

#     # Return the polygons as a JSON object
#     return jsonify(polygons)

@app.route('/process_image', methods=['POST'])
def get_polygons():
    # Get the image file from the POST request
    file = request.files['image']

    # Read the image file using OpenCV
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Get the desired width and height from the request
    width = int(request.form['width'])
    height = int(request.form['height'])

    # Resize the image
    img = cv2.resize(img, (width, height))

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold image
    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours of polygons
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create a dictionary to store the polygons
    polygons = {}

    # Extract the x y coordinates for each polygon
    for i, contour in enumerate(contours):

        if i == 0:
            continue

        # Get the x y coordinates of the current polygon
        polygon = contour.squeeze().tolist()

        # Add the polygon to the dictionary
        polygons[f'polygon{i}'] = polygon

    # Return the polygons as a JSON object
    return jsonify(polygons)

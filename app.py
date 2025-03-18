from flask import Flask, request, render_template
from PIL import Image, UnidentifiedImageError
import os
import pillow_avif  # Required for AVIF support

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'avif', 'webp', 'bmp', 'tiff', 'ico', 'heif', 'heic'}

# Set limits on dimensions
MAX_WIDTH = 1920  # Maximum width in pixels
MAX_HEIGHT = 1080  # Maximum height in pixels
MIN_WIDTH = 100  # Minimum width in pixels
MIN_HEIGHT = 100  # Minimum height in pixels

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get('photo')
        if not file or not allowed_file(file.filename):
            return "Error: Unsupported or no file uploaded!"

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            # Open and process the image
            with Image.open(filepath) as img:
                # Validate dimensions
                width = int(request.form['width'])
                height = int(request.form['height'])
                
                if width > MAX_WIDTH or height > MAX_HEIGHT:
                    return f"Error: Dimensions too large! Max allowed is {MAX_WIDTH}x{MAX_HEIGHT} pixels."
                if width < MIN_WIDTH or height < MIN_HEIGHT:
                    return f"Error: Dimensions too small! Min allowed is {MIN_WIDTH}x{MIN_HEIGHT} pixels."

                # Resize and save the image
                img = img.resize((width, height))
                resized_filepath = os.path.join(app.config['UPLOAD_FOLDER'], "resized_image.png")
                img.save(resized_filepath, "PNG")

            return f"Image resized successfully! Saved as {resized_filepath}"
        except UnidentifiedImageError:
            return "Error: Unsupported or corrupted image file."
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)

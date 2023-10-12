#import render template
import os
from flask import Flask, render_template, request, flash, url_for
from werkzeug.utils import secure_filename
import cv2
from PIL import Image

# flask is the app name here
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'webp', 'jpg', 'png', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray": 
            imgPro = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgPro)
            return newFilename
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": 
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cwebp": 
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpdf": 
            img = Image.open(f"uploads/{filename}")
            img = img.convert('RGB')
            newFilename = img.save(f"static/{filename.rsplit('.')[-2]}.pdf")
            newFilename = f"static/{filename.rsplit('.')[-2]}.pdf"
            return newFilename
        
    pass


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/instructions")
def instructions():
    return render_template('instructions.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/edit", methods = ["GET","POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return 'Error'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "Error no file is selected for editing"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")
    return render_template("index.html")

app.run(debug = True, port = 5001)

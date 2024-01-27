from multiprocessing.spawn import prepare
from re import template
from flask import Flask, flash, redirect, render_template, request, make_response, url_for
from keras.models import load_model
import cv2
import os

app = Flask(__name__)
app.secret_key = "NabilHensem"

# This is the global variables
model = None
IMAGE_FOLDER_PATH = "./images/"
TEMPLATES = {
   "home": "main.html",
   "error": "err.html",
}
FRUIT_TYPES = ["Rambutan", "Mangosteen", "Langsat", "Durian"]

# Load the model into the web-application
def load():
    # TODO: change this into proper model location
    model_path = "./ICD.model"
    global model
    model = load_model(model_path)

# Predict the image 
def predict(file_name):
    prepared_img = prepare_image(file_name)
    prediction = model.predict(prepared_img)
    return predict_display(prediction)

# Prepare for the prediction
def prepare_image(file_name):
  IMG_SIZE = 227
  img_array = cv2.imread(file_name)
  if(img_array.size or img_array.size <= 0): 
     print("Size Image is 0")
  new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
  return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

# Return the prediction into an object for easy accessible
def predict_display(prediction):
    classes = ['Class 1', 'Class 2', 'Class 3', 'Class 4']
    max = {
        "probability": 0,
        "type": "null"
    }
    for index, cls in enumerate(prediction[0]):
        probability = round(cls, 5)
        print(FRUIT_TYPES[index] + ": (" + classes[index] + ") - " + str(probability) + "\n")
        if(probability > max["probability"]):
            max["probability"] = probability
            max["type"] = FRUIT_TYPES[index]

    print("Fruit is " + max["type"]  + " with probability of " + str(max["probability"]))
    return max

    

# Upload the file and return the path of the file
def upload_to_local(file):
   folder_path = os.path.join(IMAGE_FOLDER_PATH, file.filename)
   file.save(folder_path)
   return str(folder_path)

@app.route("/")
def main():
    return render_template(TEMPLATES["home"])

@app.route("/main")
def test():
    return render_template(TEMPLATES["home"])

#  ================================
#  Upload Stuffs: handle all the upload stuffs
# ================================

def err_upload_failed():
    print("Error!")

# Probably can more than .jpg? 
ALLOWED_EXTENSION = {"jpg", "webpg", "jpeg"}

@app.route("/", methods=['POST'])
def handle_image():
    load()
    if request.method == "POST":
        
        # If the file doesn't exist, redirect back to index.html
        if 'file' not in request.files:
            err_upload_failed()
            return redirect('/')
        
        file = request.files['file']
        filename = file.filename  

        # TODO: Make sure that error exception is OK
        if filename == '':
           err_upload_failed()
           return redirect('/')

        # TODO: Make sure that error exception is OK
        if filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSION:
           err_upload_failed()
           return redirect('/')
         
        print("Filename: " +  filename)
        print("Uploading.." +  filename)
        file_path = upload_to_local(file)
        flash("Success!")
        print("Successfully Upload ✅\nFile Path: " + file_path)

        # TODO: POST the prediction rate and into the JS? 
        fruit_max = predict(file_path)
        print(fruit_max["type"])

    #  TODO: Update the page with this data by using render_template("index.html", PROBABILITIES = something, MAX = fruit_max)
    return render_template(TEMPLATES["home"], FRUIT = fruit_max["type"])
       


if __name__ == '__main__':  
  app.run(debug = True)
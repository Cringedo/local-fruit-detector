from multiprocessing.spawn import prepare
from flask import Flask, flash, redirect, render_template, request, make_response, url_for
from keras.models import load_model
import cv2

app = Flask(__name__)
app.secret_key = "GeeksForGeeks"

# This is the model variable
model = None

# Prepare for the prediction
def prepare_image(file_name):
  IMG_SIZE = 227
  img_array = cv2.imread(file_name)
  new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
  return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

# Load the model into the web-application
def load():
    # TODO: change this into proper model location
    model_path = "./ICD.model"
    global model
    model = load_model(model_path)
    example_img = "./images/durian_example.jpg"
    predict(example_img)
    
# Predict the image 
def predict(file_name):
    prepared_img = prepare_image(file_name)
    prediction = model.predict(prepared_img)
    predict_display(prediction)

def predict_display(prediction):
   classes = ['Class 1', 'Class 2', 'Class 3', 'Class 4']
   for index, cls in enumerate(prediction[0]):
      print(str(index) + " - " + str(round(cls, 5)) + "\n")

@app.route("/")
def main():
    # load()
    # predict()
    return render_template('index.html')

@app.route("/main")
def test():
    # load()
    # predict()
    return render_template('index.html')

#  ================================
#  Upload Stuffs: handle all the upload stuffs
# ================================

def err_upload_failed():
    flash("please upload a proper file")
    redirect(url_for('main'))

# Probably can more than .jpg? 
ALLOWED_EXTENSION = {"jpg"}

@app.route("/upload_image", methods=['POST'])
def handle_image():
    if request.method == "POST":
        
        # If the file doesn't exist, redirect back to index.html
        if 'file' not in request.files:
            err_upload_failed()
        
        file = request.files['file']
        filename = file.filename  

        # TODO: Make sure that error exception is OK
        if filename == '':
           err_upload_failed()

        # TODO: Make sure that error exception is OK
        if filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSION:
           err_upload_failed()

        print("File: " +  filename) 
    
    # TODO: POST the prediction rate and into the JS?  
    return "Test!"
       


if __name__ == '__main__':  
  app.run(debug = True)
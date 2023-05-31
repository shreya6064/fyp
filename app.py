from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
import tensorflow as tf
from tensorflow import keras
from werkzeug.utils import secure_filename
import PIL
from PIL import Image
import os
import pathlib
import numpy as np
import pickle

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

LOADED_MODEL = ""
with open("demographic_model_2.pkl", "rb") as file:
        LOADED_MODEL = pickle.load(file)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#three forward slashes is a relative path
#database is intiialised with settings from the app
db = SQLAlchemy(app)



@app.route("/")
def index():
    #add a comma and pass information here
    x = 5
    return render_template("index.html", x = x)




"""@app.route("/image-analysis.html")
def image_analysis():
    p = add(4,5)
    new_model = tf.keras.models.load_model('my_model.keras')
    return render_template("image-analysis.html")"""



#this is what shows up in the search bar
"""@app.route('/image-analysis')
def image_analysis():

    image = request.files["image"]
    filename = image.filename
    image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return render_template("image-analysis.html")
 """


def model_predict(img_path):
    # Here we just return 6 as a dummy prediction
    model = tf.keras.models.load_model('my_model.keras')
    img_height = 180
    img_width = 180
    class_names = ['infected', 'notinfected']
    sunflower_path = pathlib.Path(img_path)



    img = tf.keras.utils.load_img(
        sunflower_path, target_size=(img_height, img_width)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])


    if class_names[np.argmax(score)] == "infected":
        return True
    #elif class_names[np.argmax(score)] == "notinfected":
    return False



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	


@app.route('/image-analysis', methods=['GET', 'POST'])
def upload_file():
    filename = None
    prediction = None

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_path)
            #return redirect(url_for('upload_file'))
            prediction = model_predict(full_path)
            if prediction == True:
                prediction = "PCOS Detected"
            else:
                prediction = "PCOS Not Detected"

    return render_template('image-analysis.html', filename=filename, prediction=prediction)



@app.route("/gene-expression")
def gene_expression():
    return render_template("gene-expression.html")





def demographic_predict(follicle_r, follicle_l, hair_growth, skin_darkening, weight_gain, cycle, fast_food, bmi, pimples, weight):
    # Currently, this function just returns 6 as a placeholder.
    # You should replace this with your actual prediction code.

    # Load the random forest classifier model
    
    #n1 = np.array((44.6, 19.3, 2, 0, 0, 0, 0, 1, 3, 3))
    #n1 = np.array((68.8, 25.27, 2, 0, 0, 0, 1, 1, 13, 15))
    if cycle == True:
        cycle=2
    else:
        cycle=4

    n1 = np.array((float(weight), float(bmi), int(cycle), float(bool(weight_gain)), float(bool(hair_growth)), float(bool(skin_darkening)), float(bool(pimples)), float(bool(fast_food)), int(follicle_l), int(follicle_r)))


    # Use the loaded model for predictions
    prediction = LOADED_MODEL.predict(n1.reshape(1,-1))[0]
    #predictions[0]
    #return 6
    if prediction == 0:
        return "PCOS Not Detected"
    
    return "PCOS Detected"




@app.route("/demographic-model",  methods=['GET', 'POST'])
def demographic():
    dem_pred = None
    if request.method == 'POST':
        follicle_r = request.form['follicle_r']
        follicle_l = request.form['follicle_l']
        hair_growth = request.form['hair_growth']
        skin_darkening = request.form['skin_darkening']
        weight_gain = request.form['weight_gain']
        cycle = request.form['cycle']
        fast_food = request.form['fast_food']
        bmi = request.form['bmi']
        pimples = request.form['pimples']
        weight = request.form['weight']

        parameters = {"follicle_r" : follicle_r, 
                      "follicle_l" : follicle_l,
                      }
        dem_pred = demographic_predict(follicle_r, follicle_l, hair_growth, skin_darkening, weight_gain, cycle, fast_food, bmi, pimples, weight)
        return render_template('dem_prediction.html', dem_pred=dem_pred, form_data=request.form)

    return render_template("demographic.html", form_data=request.form)


@app.route("/test")
def test():
    form_data = {
    "follicle_r": 12,
    "follicle_l": 10,
    "hair_growth": "Yes",
    "skin_darkening": "No",
    "weight_gain": "Yes",
    "cycle": 28,
    "fast_food": "No",
    "bmi": 22.5,
    "pimples": "Yes",
    "weight": 65.0
}


    return render_template('dem_prediction.html', dem_pred="PCOS Detected", form_data=form_data)


if __name__=="__main__":
    app.run(debug=True)
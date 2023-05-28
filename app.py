from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#three forward slashes is a relative path
#database is intiialised with settings from the app
db = SQLAlchemy(app)

"""
class Idk(db.Model):
    id = db.Column(db.Integer, primary_key=True)

"""


@app.route("/", methods=['POST', 'GET'])
def index():
    #add a comma and pass information here
    x = 5
    return render_template("index.html", x = x)


def add(x,y):
    return x+y


@app.route("/image-analysis.html")
def image_analysis():
    p = add(4,5)
    new_model = tf.keras.models.load_model('my_model.keras')
    return render_template("image-analysis.html", p=p)

@app.route("/gene-expression.html")
def gene_expression():
    return render_template("gene-expression.html")


if __name__=="__main__":
    app.run(debug=True)
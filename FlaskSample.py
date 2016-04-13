from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("quiz.html")

@app.route('/', methods=['POST'])
def my_form_post():

    FilePath = request.form['FilePath']
    FromTime =request.form['FromTime']
    ToTime = request.form['ToTime']
    processed_text = FilePath.upper() + " " + FromTime.upper() + " " + ToTime.upper()
    return processed_text

if __name__ == '__main__':
    app.debug = True
    app.run()
import random
import string 
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def html():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)








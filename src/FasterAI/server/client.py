from flask import Blueprint, render_template

client = Blueprint("client", __name__)

@client.route("/")
def index():
    return render_template("index.html")
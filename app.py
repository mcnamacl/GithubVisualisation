from github import Github
from flask import Flask, request, render_template, jsonify
import sys

app = Flask(__name__)

g = Github("mcnamacl", "password")
userName = g.get_user().name

@app.route("/")
def index():
    return render_template("index.html")

def getFollowers():
    index = 0
    for follower in g.get_user().get_followers():
        print(follower, file=sys.stderr)
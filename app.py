from github import Github
from flask import Flask, request, render_template, jsonify
from collections import defaultdict, OrderedDict
import collections
import sys
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def createFlowMatrix():
    repoLanguages = {}
    with open('repoLanguages.txt') as json_file:
        repoLanguages = json.load(json_file)

    userLanguages = {}
    with open('userLanguages.txt') as json_file:
        userLanguages = json.load(json_file)
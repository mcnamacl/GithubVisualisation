from github import Github
from flask import Flask, request, render_template, jsonify
from collections import defaultdict, OrderedDict
import collections
import sys
import json

app = Flask(__name__)

@app.route("/")
def index():
    matix = createFlowMatrix()
    return render_template("index.html")

@app.route("/piecharts")
def picecharts():
    compPiechartVals = createCompanyPieChart()
    langPiechartVales = createLanguagePieChart()
    return render_template("piecharts.html")

def createFlowMatrix():
    combinedLanguages = readInFile('combinedLanguages.txt')
    combinedCompanies = readInFile('combinedCompanies.txt')

def createCompanyPieChart():
    repoCompanies = readInFile('repoCompanies.txt')
    userCompanies = readInFile('userCompanies.txt')

def createLanguagePieChart():
    userLanguages = readInFile('userLanguages.txt')
    repoLanguages = readInFile('repoLanguages.txt')

def readInFile(fileName):
    with open(fileName) as json_file:
        return json.load(json_file)

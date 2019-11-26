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
    combinedPiechart = createCombinedPieChart()
    return render_template("piecharts.html")

def createFlowMatrix():
    corrCompLang = readInFile('corrCompanyLanguages.txt')
    getMaxNumberLanguageTuples(corrCompLang)

def getMaxNumberLanguageTuples(compLangArr):
    greatestLen = 0
    biggestComp = ""
    for comp in compLangArr:
        if len(compLangArr[comp]) > greatestLen:
            greatestLen = len(compLangArr[comp])
            biggestComp = comp
    print(biggestComp, file=sys.stderr)

def createCompanyPieChart():
    repoCompanies = readInFile('repoCompanies.txt')
    userCompanies = readInFile('userCompanies.txt')

def createLanguagePieChart():
    userLanguages = readInFile('userLanguages.txt')
    repoLanguages = readInFile('repoLanguages.txt')

def createCombinedPieChart():
    combinedLanguages = readInFile('combinedLanguages.txt')
    combinedCompanies = readInFile('combinedCompanies.txt')

def readInFile(fileName):
    with open(fileName) as json_file:
        return json.load(json_file)

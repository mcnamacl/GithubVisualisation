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
    topTenLanguages = getTopTenLanguages(compLangArr)
    
# Gets top ten language by use per company
def getTopTenLanguages(compLangArr):
    topLanguages = {}
    for comp in compLangArr:
        for lang in compLangArr[comp]:
            if lang not in topLanguages:
                topLanguages[lang] = 1
            else:
                num = topLanguages[lang]
                num = num + 1
                topLanguages[lang] = num
    sortedLanguages = OrderedDict(sorted(topLanguages.items(), key=lambda x: x[1], reverse = True))
    topTenLanguages = []
    index = 0
    for lang in sortedLanguages:
        topTenLanguages.append(lang)
        index = index + 1
        if index == 10:
            break
    return topTenLanguages

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

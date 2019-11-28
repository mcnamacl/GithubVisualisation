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
    compLangArr = readInFile('corrCompanyLanguages.txt')
    topTenLanguages = getTopTenLanguages(compLangArr)
    topTenCompanies = getTopTenCompanies(compLangArr)
    jsonMatrix = {}
    rowIndex = 1
    for comp in topTenCompanies:
        jsonMatrix[str(rowIndex)] = []
        rowList = []
        for lang in topTenLanguages:
            if lang in compLangArr[comp]:
                num = compLangArr[comp][lang]
                rowList.append(num)
            else:
                rowList.append(0)
        jsonMatrix[str(rowIndex)].append(rowList)
        rowIndex = rowIndex + 1

    print(json.dumps(jsonMatrix), file=sys.stderr)

    
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

# Gets top ten companies by variety
def getTopTenCompanies(compLangArr):
    companies = {}
    for comp in compLangArr:
        companies[comp] = len(compLangArr[comp])
    sortedLanguages = OrderedDict(sorted(companies.items(), key=lambda x: x[1], reverse = True))
    topTenCompanies = []
    index = 0
    for lang in sortedLanguages:
        topTenCompanies.append(lang)
        index = index + 1
        if index == 10:
            break
    return topTenCompanies

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

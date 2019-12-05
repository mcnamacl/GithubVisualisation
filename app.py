from github import Github
from flask import Flask, request, render_template, jsonify
from collections import defaultdict, OrderedDict
import collections
import sys
import json

app = Flask(__name__)

@app.route("/")
def index():
    matrix, xAxis, yAxis = createFlowMatrix()
    labels = xAxis + yAxis
    return render_template("index.html", matrix=matrix, labels=labels)

@app.route("/piecharts")
def picecharts():
    compPiechart = createRepoCompanyPieChart()
    langPiechart = createRepoLanguagePieChart()
    combinedCompPiechart = createCombinedCompanyPieChart()
    combinedLangPiechart = createCombinedLanguagePieChart()
    return render_template("piecharts.html", compPiechart=compPiechart, langPiechart=langPiechart, combinedCompPiechart=combinedCompPiechart, combinedLangPiechart=combinedLangPiechart)

def createFlowMatrix():
    compLangArr = readInFile('corrCompanyLanguages.txt')
    topTenLanguages = getTopTenLanguages(compLangArr)
    topTenCompanies = getTopTenCompanies(compLangArr)
    jsonMatrix = {}
    jsonCompanies = []
    jsonLanguages = []
    rowIndex = 1
    gotLang = False
    for comp in topTenCompanies:
        jsonMatrix[str(rowIndex)] = []
        rowList = []
        for lang in topTenLanguages:
            if lang in compLangArr[comp]:
                num = compLangArr[comp][lang]
                rowList.append(num)
            else:
                rowList.append(0)
            if not gotLang:
                jsonLanguages.append(lang)
        jsonMatrix[str(rowIndex)].append(rowList)
        rowIndex = rowIndex + 1
        jsonCompanies.append(comp)
        gotLang = True

    return jsonMatrix, jsonCompanies, jsonLanguages

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

def createRepoCompanyPieChart():
    return readInFile('repoCompanies.txt')

def createRepoLanguagePieChart():
    return readInFile('repoLanguages.txt')

def createCombinedCompanyPieChart():
    return readInFile('combinedCompanies.txt')

def createCombinedLanguagePieChart():
    return readInFile('combinedLanguages.txt')

def readInFile(fileName):
    with open(fileName) as json_file:
        return json.load(json_file)

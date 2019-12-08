from github import Github
from flask import Flask, request, render_template, jsonify
from collections import defaultdict, OrderedDict
import collections
import sys
import json
import numpy
import random

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    num = 10
    newNum = request.form.get("numOfCorr")
    if newNum is not None:
        newNum = int(newNum)
        if isNumber(newNum) and newNum > 0 and newNum < 30:
            num = newNum
    matrix, xAxis, yAxis = createFlowMatrix(num)
    labels = xAxis + yAxis
    complang = createLabelsColoursCSV(labels, num)
    return render_template("index.html", matrix=matrix, complang=complang)


@app.route("/piecharts", methods=["POST", "GET"])
def picecharts():
    piechart = None
    title = ""
    if request.method == "POST":
        piechartType = request.form.get("piechartChoice")
        if piechartType == "compRepo":
            piechart = createRepoCompanyPieChart()
            title = "Top Repository Breakdown by Company"
        elif piechartType == "langRepo":
            piechart = createRepoLanguagePieChart()
            title = "Top Repository Breakdown by Language"
        elif piechartType == "combRepo":
            piechart = createCombinedCompanyPieChart()
            title = "Combined Top Repository/Top User Breakdown by Company"
        elif piechartType == "combLang":
            piechart = createCombinedLanguagePieChart()
            title = "Combined Top Repository/Top User Breakdown by Language"
    return render_template("piecharts.html", piechart=piechart, title=title)

def isNumber(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def createFlowMatrix(finalNum):
    compLangArr = readInFile("corrCompanyLanguages.txt")
    topXLanguages = getTopXNumLanguages(compLangArr, finalNum)
    topXCompanies = getTopXNumCompanies(compLangArr, finalNum)
    jsonMatrix = {}
    jsonCompanies = []
    jsonLanguages = []
    rowIndex = 1
    gotLang = False
    for comp in topXCompanies:
        jsonMatrix[str(rowIndex)] = []
        rowList = []
        for lang in topXLanguages:
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

    finalMatrix = createFinalMatrix(jsonMatrix, finalNum)
    return finalMatrix, jsonCompanies, jsonLanguages


# Gets top X num of languages by use per company
def getTopXNumLanguages(compLangArr, finalNum):
    topLanguages = {}
    for comp in compLangArr:
        for lang in compLangArr[comp]:
            if lang not in topLanguages:
                topLanguages[lang] = 1
            else:
                num = topLanguages[lang]
                num = num + 1
                topLanguages[lang] = num
    sortedLanguages = OrderedDict(
        sorted(topLanguages.items(), key=lambda x: x[1], reverse=True)
    )
    topXLanguages = []
    index = 0
    for lang in sortedLanguages:
        topXLanguages.append(lang)
        index = index + 1
        if index == finalNum:
            break
    return topXLanguages


# Gets top X num of companies by variety
def getTopXNumCompanies(compLangArr, finalNum):
    companies = {}
    for comp in compLangArr:
        companies[comp] = len(compLangArr[comp])
    sortedLanguages = OrderedDict(
        sorted(companies.items(), key=lambda x: x[1], reverse=True)
    )
    topXCompanies = []
    index = 0
    for lang in sortedLanguages:
        topXCompanies.append(lang)
        index = index + 1
        if index == finalNum:
            break
    return topXCompanies


def createFinalMatrix(matrix, finalNum):
    rangeNum = finalNum * 2
    finalMatrix = [[0] * rangeNum for i in range(rangeNum)]
    index = 0
    for x in matrix:
        j = finalNum
        while j < rangeNum:
            finalMatrix[index][j] = matrix[x][0][j - finalNum]
            j = j + 1
        index = index + 1

    index = 0
    for x in matrix:
        j = finalNum
        while j < rangeNum:
            finalMatrix[j][index] = matrix[x][0][j - finalNum]
            j = j + 1
        index = index + 1
        
    return finalMatrix


def createLabelsColoursCSV(labels, finalNum):
    finalLabels = [[0] * 2 for i in range(finalNum * 2)]
    index = 0
    for label in labels:
        finalLabels[index][0] = label
        finalLabels[index][1] = getRandomHex()
        index = index + 1

    return finalLabels


def getRandomHex():
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    return "#" + hex_number[2:]


def createRepoCompanyPieChart():
    return readInFile("repoCompanies.txt")


def createRepoLanguagePieChart():
    return readInFile("repoLanguages.txt")


def createCombinedCompanyPieChart():
    return readInFile("combinedCompanies.txt")


def createCombinedLanguagePieChart():
    return readInFile("combinedLanguages.txt")


def readInFile(fileName):
    with open(fileName) as json_file:
        return json.load(json_file)

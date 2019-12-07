from github import Github
from flask import Flask, request, render_template, jsonify
from collections import defaultdict, OrderedDict
import collections
import sys
import json
import numpy
import random

app = Flask(__name__)


@app.route("/")
def index():
    matrix, xAxis, yAxis = createFlowMatrix()
    labels = xAxis + yAxis
    complang = createLabelsColoursCSV(labels)
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


def createFlowMatrix():
    compLangArr = readInFile("corrCompanyLanguages.txt")
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
        print(comp, file=sys.stderr)
        for lang in topTenLanguages:
            if lang in compLangArr[comp]:
                num = compLangArr[comp][lang]
                rowList.append(num)
                print(lang + " " + str(num), file=sys.stderr)
            else:
                rowList.append(0)
                print(lang, file=sys.stderr)
            if not gotLang:
                jsonLanguages.append(lang)
        jsonMatrix[str(rowIndex)].append(rowList)
        rowIndex = rowIndex + 1
        jsonCompanies.append(comp)
        gotLang = True
        print("\n", file=sys.stderr)

    finalMatrix = createFinalMatrix(jsonMatrix)
    return finalMatrix, jsonCompanies, jsonLanguages


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
    sortedLanguages = OrderedDict(
        sorted(topLanguages.items(), key=lambda x: x[1], reverse=True)
    )
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
    sortedLanguages = OrderedDict(
        sorted(companies.items(), key=lambda x: x[1], reverse=True)
    )
    topTenCompanies = []
    index = 0
    for lang in sortedLanguages:
        topTenCompanies.append(lang)
        index = index + 1
        if index == 10:
            break
    return topTenCompanies


def createFinalMatrix(matrix):
    finalMatrix = [[0] * 20 for i in range(20)]
    index = 0
    for x in matrix:
        j = 10
        while j < 20:
            finalMatrix[index][j] = matrix[x][0][j - 10]
            j = j + 1
        index = index + 1

    index = 0
    for x in matrix:
        j = 10
        while j < 20:
            finalMatrix[j][index] = matrix[x][0][j - 10]
            j = j + 1
        index = index + 1
        
    return finalMatrix


def createLabelsColoursCSV(labels):
    finalLabels = [[0] * 2 for i in range(21)]
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

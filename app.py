from github import Github
from flask import Flask, request, render_template, jsonify
from collections import defaultdict, OrderedDict
import collections
import sys
import json

app = Flask(__name__)

g = Github("mcnamacl", "password")
userName = g.get_user().name

@app.route("/")
def index():
    #repos = getRepos(g.get_user())
    #corrFollowersRepos(g.get_user())
    #topRepos = getTopRepos()
    chordChartFour()
    return render_template("index.html")

def corrFollowersRepos(user):
    followers = getFollowers(user)
    result = {}
    for followerIt in followers:
        follower = followers[followerIt]
        result[str(follower)] = {}
        numFollower = follower.get_followers().totalCount
        numRepo = follower.get_repos().totalCount
        tmp = {numFollower : numRepo}
        result[str(follower)] = tmp
    print(json.dumps(result), file=sys.stderr)

def getRepos(user):
    repos = {}
    index = 0
    for repo in user.get_repos():
        repos[str(index)] = repo.name
        index = index + 1
    return repos

def getFollowers(user):
    followers = {}
    index = 0
    for follower in user.get_followers():
        followers[str(index)] = follower
        index = index + 1
    return followers

def getTopRepos():
    return g.search_repositories(query='stars:>=500', sort='stars', order='desc')[:100]

def getTopUsersByFollowers():
    return g.search_users(query='followers:>=1000', sort='followers', order='desc')[:100]

def languagesInRepos(repos):
    languages = {}
    for repo in repos:
        language = repo.language
        if language not in languages:
            languages[language] = 1
        else:
            num = languages[language]
            num = num + 1
            languages[language] = num
    return languages

def getUserTopLanguage(user):
    repos = user.get_repos()[:10]
    languages = languagesInRepos(repos)
    sortedLanguages = OrderedDict(sorted(languages.items(), key=lambda x: x[1]))
    return sortedLanguages.popitem()

def chordChartFour():
    topRepos = getTopRepos()
    topUsers = getTopUsersByFollowers()
    repoLanguages = languagesInRepos(topRepos)

    for topUser in topUsers:
        getUserTopLanguage(topUser)

    print(json.dumps(repoLanguages), file=sys.stderr)

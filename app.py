from github import Github
from flask import Flask, request, render_template, jsonify
import sys

app = Flask(__name__)

g = Github("mcnamacl", "password")
userName = g.get_user().name

@app.route("/")
def index():
    repos = getRepos()
    return render_template("index.html", repos=repos)

def getRepos():
    repos = {}
    index = 0
    for repo in g.get_user().get_repos():
        repos[str(index)] = repo.name
        index = index + 1
    return repos

def getFollowers():
    followers = {}
    index = 0
    for follower in g.get_user().get_followers():
        followers[str(index)] = follower
        index = index + 1
from github import Github
from flask import Flask, request, render_template, jsonify
from collections import defaultdict
import sys
import json

app = Flask(__name__)

g = Github("mcnamacl", "password")
userName = g.get_user().name

@app.route("/")
def index():
    repos, numOfRepos = getRepos(g.get_user())
    followers, numOfFollowers = getFollowers(g.get_user())
    return render_template("index.html", repos=repos)

def corrFollowersRepos(user):
    repos, numOfRepos = getRepos(user)
    followers, numOfFollowers = getFollowers(user)
    for follower in followers:
        _, numFollower = getFollowers(followers[follower])
        _, numRepo = getRepos(followers[follower])

def getRepos(user):
    repos = {}
    index = 0
    for repo in user.get_repos():
        repos[str(index)] = repo.name
        index = index + 1
    return repos, index

def getFollowers(user):
    followers = {}
    index = 0
    for follower in user.get_followers():
        followers[str(index)] = follower
        index = index + 1
    return followers, index
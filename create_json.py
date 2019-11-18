from github import Github
from collections import defaultdict, OrderedDict
import collections
import sys
import json

g = Github("mcnamacl", "password")
userName = g.get_user().name

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
    userLanguages = {}

    for topUser in topUsers:
        language = getUserTopLanguage(topUser)
        language = language[0]
        if language not in userLanguages:
            userLanguages[language] = 1
        else:
            num = userLanguages[language]
            num = num + 1
            userLanguages[language] = num

    repoLanguages = OrderedDict(sorted(repoLanguages.items(), key=lambda x: x[1], reverse=True))
    userLanguages = OrderedDict(sorted(userLanguages.items(), key=lambda x: x[1], reverse=True))

    with open('repoLanguages.txt', 'w') as outfile:
        json.dump(repoLanguages, outfile)

    with open('userLanguages.txt', 'w') as outfile:
        json.dump(userLanguages, outfile)

if __name__ == '__main__':
    chordChartFour()
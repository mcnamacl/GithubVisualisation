from github import Github
from collections import defaultdict, OrderedDict, Counter
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
    return g.search_repositories(query='stars:>=500', sort='stars', order='desc')[:10]

def getTopUsersByFollowers():
    return g.search_users(query='followers:>=1000', sort='followers', order='desc')[:10]

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

def languagesByUsers(topUsers):
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
    return userLanguages

def getUserTopLanguage(user):
    repos = user.get_repos()[:10]
    languages = languagesInRepos(repos)
    sortedLanguages = OrderedDict(sorted(languages.items(), key=lambda x: x[1]))
    return sortedLanguages.popitem()

def getRepoTopCompanies(repos):
    companies = {}
    for repo in repos:
        company = getCompanyName(str(repo.organization))
        if company not in companies:
            companies[company] = 1
        else:
            num = companies[company]
            num = num + 1
            companies[company] = num
    return companies

def getUserTopCompanies(topUsers):
    companies = {}
    for user in topUsers:
        numOfCompanies = user.get_orgs().totalCount
        if numOfCompanies is not 0:
            company = getCompanyName(str(user.get_orgs()[0]))
        else:
            company = 'None'
        if company not in companies:
            companies[company] = 1
        else:
            num = companies[company]
            num = num + 1
            companies[company] = num
    return companies

def getCompanyName(company):
    company = company.replace('Organization(login=\"', '')
    return company.replace('\")', '')

def getCompanyLanguages(topRepos, topUsers):
    compLang = {}

    for repo in topRepos:
        company = getCompanyName(str(repo.organization))
        language = repo.language
        if company not in compLang:
            compLang[company] = {}
            compLang[company][language] = 1
        elif language not in compLang[company]:
            compLang[company][language] = 1
        else:
            num = compLang[company][language]
            num = num + 1
            compLang[company][language] = num

    for user in topUsers:
        numOfCompanies = user.get_orgs().totalCount
        if numOfCompanies is not 0:
            company = getCompanyName(str(user.get_orgs()[0]))
        else:
            company = 'None'
        language = getUserTopLanguage(user)
        if company not in compLang:
            compLang[company] = {}
            compLang[company][language] = 1
        elif language not in compLang[company]:
            compLang[company][language] = 1
        else:
            num = compLang[company][language]
            num = num + 1
            compLang[company][language] = num

    print(compLang)

def chordChart():
    topRepos = getTopRepos()
    topUsers = getTopUsersByFollowers()

    getCompanyLanguages(topRepos, topUsers)

    # repoLanguages = languagesInRepos(topRepos)
    # userLanguages = languagesByUsers(topUsers)
    
    # combinedLanguages = Counter(repoLanguages) + Counter(userLanguages)

    # combinedLanguages = OrderedDict(sorted(combinedLanguages.items(), key=lambda x: x[1], reverse=True))
    # userLanguages = OrderedDict(sorted(userLanguages.items(), key=lambda x: x[1], reverse=True))
    # repoLanguages = OrderedDict(sorted(repoLanguages.items(), key=lambda x: x[1], reverse=True))

    # topRepoCompanies = getRepoTopCompanies(topRepos)
    # topUserCompanies = getUserTopCompanies(topUsers)

    # combinedCompanies = Counter(topRepoCompanies) + Counter(topUserCompanies)

    # combinedCompanies = OrderedDict(sorted(combinedCompanies.items(), key=lambda x: x[1], reverse=True))
    # topRepoCompanies = OrderedDict(sorted(topRepoCompanies.items(), key=lambda x: x[1], reverse=True))
    # topUserCompanies = OrderedDict(sorted(topUserCompanies.items(), key=lambda x: x[1], reverse=True))

    # with open('repoLanguages.txt', 'w') as outfile:
    #     json.dump(repoLanguages, outfile)

    # with open('userLanguages.txt', 'w') as outfile:
    #     json.dump(userLanguages, outfile)
    
    # with open('combinedLanugages.txt', 'w') as outfile:
    #     json.dump(combinedLanguages, outfile)

    # with open('repoCompanies.txt', 'w') as outfile:
    #     json.dump(topRepoCompanies, outfile)

    # with open('userCompanies.txt', 'w') as outfile:
    #     json.dump(topUserCompanies, outfile)
    
    # with open('combinedCompanies.txt', 'w') as outfile:
    #     json.dump(combinedCompanies, outfile)

if __name__ == '__main__':
    chordChart()
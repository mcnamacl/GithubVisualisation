from github import Github
from collections import defaultdict, OrderedDict, Counter
import collections
import sys
import json

g = Github("mcnamacl", "password")
userName = g.get_user().name

# Returns the top 300 repositories by number of stars.
def getTopRepos():
    return g.search_repositories(query='stars:>=500', sort='stars', order='desc')[:300]

# Returns the top 300 users by number of users.
def getTopUsersByFollowers():
    return g.search_users(query='followers:>=1000', sort='followers', order='desc')[:300]

# Creates a dictionary of languages and number of times used by repos.
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

# Creates a dictionary of languages and number of times used by users. 
def languagesByUsers(topUsers):
    userLanguages = {}
    for topUser in topUsers:
        language = getUserTopLanguage(topUser)
        if language is None:
            language = "None"
        else:
            language = language[0]
        if language not in userLanguages:
            userLanguages[language] = 1
        else:
            num = userLanguages[language]
            num = num + 1
            userLanguages[language] = num
    return userLanguages

# Gets the top language used by a user from 10 of their repos.
def getUserTopLanguage(user):
    if user.get_repos().totalCount > 10:
        repos = user.get_repos()[:10]
    else:
        repos = user.get_repos()
    languages = languagesInRepos(repos)
    if not languages:
        return None
    else:
        sortedLanguages = OrderedDict(sorted(languages.items(), key=lambda x: x[1], reverse = True))
        return sortedLanguages.popitem()

# Creates dictionary of companies and the number of times they are associated with the top repos.
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

# Creates a dictionary of companies and number of times they are associated with the top users.
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

# Creates correlation dictionary between company and languages used.
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
        if language is None:
            language = 'Null'
        else:
            language = language[0]
        if company not in compLang:
            compLang[company] = {}
            compLang[company][language] = 1
        elif language not in compLang[company]:
            compLang[company][language] = 1
        else:
            num = compLang[company][language]
            num = num + 1
            compLang[company][language] = num

    return compLang

def main():
    topRepos = getTopRepos()
    topUsers = getTopUsersByFollowers()

    repoLanguages = languagesInRepos(topRepos)
    userLanguages = languagesByUsers(topUsers)
    
    combinedLanguages = Counter(repoLanguages) + Counter(userLanguages)

    combinedLanguages = OrderedDict(sorted(combinedLanguages.items(), key=lambda x: x[1], reverse=True))
    userLanguages = OrderedDict(sorted(userLanguages.items(), key=lambda x: x[1], reverse=True))
    repoLanguages = OrderedDict(sorted(repoLanguages.items(), key=lambda x: x[1], reverse=True))

    topRepoCompanies = getRepoTopCompanies(topRepos)
    topUserCompanies = getUserTopCompanies(topUsers)

    combinedCompanies = Counter(topRepoCompanies) + Counter(topUserCompanies)

    combinedCompanies = OrderedDict(sorted(combinedCompanies.items(), key=lambda x: x[1], reverse=True))
    topRepoCompanies = OrderedDict(sorted(topRepoCompanies.items(), key=lambda x: x[1], reverse=True))
    topUserCompanies = OrderedDict(sorted(topUserCompanies.items(), key=lambda x: x[1], reverse=True))

    corrCompanyLanguages = getCompanyLanguages(topRepos, topUsers)

    with open('repoLanguages.txt', 'w') as outfile:
        json.dump(repoLanguages, outfile)

    with open('userLanguages.txt', 'w') as outfile:
        json.dump(userLanguages, outfile)
    
    with open('combinedLanugages.txt', 'w') as outfile:
        json.dump(combinedLanguages, outfile)

    with open('repoCompanies.txt', 'w') as outfile:
        json.dump(topRepoCompanies, outfile)

    with open('userCompanies.txt', 'w') as outfile:
        json.dump(topUserCompanies, outfile)
    
    with open('combinedCompanies.txt', 'w') as outfile:
        json.dump(combinedCompanies, outfile)

    with open('corrCompanyLanguages.txt', 'w') as outfile:
        json.dump(corrCompanyLanguages, outfile)    

if __name__ == '__main__':
    main()
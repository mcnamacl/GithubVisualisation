from github import Github

g = Github("mcnamacl", "password")

name = g.get_user().name
print(name)


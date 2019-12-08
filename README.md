# GithubDataVisualisation

The application runs on localhost:5000 by executing python -m flask run while in the source folder. 

The commit relating to first access of the github API: efc861c76652afacc6b0802f1f129cc7f372268a.

-----------------------------------------------------------------------------
# Overview of Idea
The basic idea is to demonstate the correlation between companies and the languages used using information gained from the top repos and top users on the site.

## Data processing
Step 1:
Through the Github API I get 300 of the top rated Github Repositories by number of stars and 300 of the top users by
number of followers.

Step 2 - Languages:
Dealing with the Repo: I create a json file that has a key being the language and the value being the number of repos that
primarily use that language.

Dealing with the User: This was slightly more difficult to achieve. Again through the Github API I receive a slice of 10 of 
their repos and get the most used language within those 10. I then again create a json file containing key of language 
and value being number of users that most use that language.

Step 3 - Companies:
Using a process similar to the one above, I get the the company affiliated with a repo/user and then the number of other repos/users that associate with that company creating two seperate key value json files. One for user and one for repo.

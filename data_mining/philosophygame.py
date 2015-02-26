#wikipedia Philosophy Game
from pattern.web import *
from bs4 import BeautifulSoup as BS

w = Wikipedia()
visited = [] #keeps track of visited sites so articles don't loop
def SearchingforPhilosophy(startarticle):
    """Recursive function that returns the number of times it
    has to try in order to get to Philosophy"""
    searchword = startarticle.lower() #so I can compare without case issues
    if searchword in visited: #check if we're looping through two articles
        return -1 #error message
    visited.append(searchword) #now we've seen it. 
    title = w.search(searchword) #search wikipedia for it. 
    # get all the links in the article
    if not title:
        return -1
    soup = BS(title.source)

    #get all the links in the article that aren't:
    # files, audio files, pictures or non-alphanumeric characters
    #Stop space confusion by checking for alphanumericism after taking away spaces
    for link in soup.find_all('p')[0].find_all('a'):
        print link
        if link['href'][:5] != "/wiki" or ":" in link['href'] or not link.string.replace(" ","").isalnum():
            continue #do the next for loop, forget this one. 
        link = link.string.lower() #to be able to compare
        print link #because this takes long to compile, this shows that the function is working
        if link == "philosophy": #this is the goal
            return 1 #the return is the amount of links I was at before, so this adds one to the base case
        elif link != searchword: #because sometimes the link and searchword are the same
            found = SearchingforPhilosophy(link) #recursively ask for the function to redo this with the new
            # word and new first link until it reaches philosophy in the earlier if statement
            if found == -1: #Sometimes they're errors. Continue to next case
                continue
            else: #This is adding up all the times it works out (how many first links I click)
                return found + 1
    return -1
#Show me the result of searching:    
print SearchingforPhilosophy('Death')
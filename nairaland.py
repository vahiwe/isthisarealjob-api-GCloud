import requests
import urllib
from textblob import TextBlob
from bs4 import BeautifulSoup

WordList = []

def percentage(part, whole):
    """function to calculate percentage"""
    return round((100 * float(part)/float(whole)),2)


def word_count(string):
    """function to return count of comments"""
    counts = dict()
    words = string.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return len(counts)


def search_item(search_term, next=False, page=0,  board=0):
    """function to search and return comments"""
    if next == False:
        page = requests.get("https://www.nairaland.com/search?q=" + urllib.parse.quote_plus(str(search_term)) + "&board="+str(board))
    else:
        page = requests.get("https://www.nairaland.com/search/"
                            + str(search_term) + "/0/"+str(board)+"/0/1" + str(page))
    soup = BeautifulSoup(page.content, 'html.parser')

    comments = soup.findAll("div", {"class": "narrow"})

    return comments


def add_to_word_list(strings):
    """function to add all comments to Wordlist"""
    WordList
    k = 0
    while k < len(strings):
        if word_count(strings[k].text) > 1:
            WordList.append(strings[k].text)
        k += 1


def nairasearch(searchTerm):
    board = 29
    try:
        j = 0
        while j < 20:
            if j == 0:
                nextItem = False
            else:
                nextItem = True
            commentsCurrent = search_item(searchTerm, nextItem, j,  board)
            add_to_word_list(commentsCurrent)
            j += 1
    except:
        negative = 50
        return negative

    polarity = 0
    positive = 0
    negative = 0
    neutral = 0


    previous = []

    for tweet in WordList:
        if tweet in previous:
            continue
        previous.append(tweet)
        analysis = TextBlob(tweet)
        """evaluating polarity of comments"""
        polarity += analysis.sentiment.polarity

        if (analysis.sentiment.polarity == 0):
            neutral += 1
        elif (analysis.sentiment.polarity < 0.00):
            negative += 1
        elif (analysis.sentiment.polarity > 0.0):
            positive += 1

    noOfSearchTerms = positive + negative + neutral

    positive = percentage(positive, noOfSearchTerms)
    negative = percentage(negative, noOfSearchTerms)
    neutral = percentage(neutral, noOfSearchTerms)

    return negative

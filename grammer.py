from gingerit.gingerit import GingerIt
import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words("english")


# check for grammer and spelling errors and return the number of corrections
def check(filename):
    f = word(filename, 'sentence')
    corrections = 0
    for s in f:
        g = GingerIt()
        h = g.parse(s)
        corrections += len(h['corrections'])
    return corrections

def word(filename, final_type): # function to tokenize text 
        tok_sent = nltk.sent_tokenize(filename)
        tok_word = []
        for s in tok_sent:
            tok_word.append(nltk.word_tokenize(s))
        final_text = []
        for w in tok_word:
            if w not in stop_words:
                final_text.append(w)
        if final_type == 'sentence':
            return tok_sent
        elif final_type == 'word':
            return final_text
""" Analyzes the word frequencies in a book downloaded from
    Project Gutenberg """

import string

def get_word_list(file_name):
    """ Reads the specified project Gutenberg book.  Header comments,
        punctuation, and whitespace are stripped away.  The function
        returns a list of the words used in the book as a list.
        All words are converted to lower case.
    """
  #  new_book = []
    f = open(file_name, 'r')
    lines = f.readlines()
    current_line = 0
    book = []

    while lines[current_line+1].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
        current_line += 1
        lines = lines[current_line+1:]
        for line in lines: 
              book.append(line.strip().lower().split(" "))
    return book

def get_top_n_words(word_list, n):
    """ Takes a list of words as input and returns a list of the n most frequently
        occurring words ordered from most to least frequently occurring.

        word_list: a list of words (assumed to all be in lower case with no
                    punctuation
        n: the number of words to return
        returns: a list of n most frequently occurring words ordered from most
                 frequently to least frequentlyoccurring
    """
    word_popularity = {}
    all_values = []
    pop_words = []
    for line in word_list:
        #creates dictionary of words and how many times they appear in text
        for word in line:
            if ','or  '' or '.' or '?' or '!' not in word:
                if word in word_popularity:
                    val = word_popularity.get(word)
                    val += 1
                    word_popularity[word] = val
                else:
                    word_popularity[word] = 1
    for key in word_popularity:
        #sorts the amount the words appear, most to least
        all_values.append(word_popularity[key])
        all_values.sort()
    biggest_values = all_values[::-1]
    #take only the top n words
    top_n_words = biggest_values[0:n]
    for value in top_n_words:
        #find the words that correspond to these values
        for key in word_popularity:
            if word_popularity.get(key) == value:
                pop_words.append([key, value])
            else:
                continue
    return pop_words
#uncomment to just test this function
#print get_word_list("mobydick.txt")

#second function, using the first
print get_top_n_words(get_word_list("mobydick.txt"), 50)
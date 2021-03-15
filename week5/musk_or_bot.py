import random

import pandas

raw_tweets = pandas.read_csv('https://raw.githubusercontent.com/robeverest/cs1010/master/data/elonmusk-full.csv')
elon_tweets = list(map(str, list(raw_tweets.tweet)))

def generate_word_map(prefix_length):
    elon_word_map = {}
    for tweet in elon_tweets:
        prefix = tuple()
        for word in tweet.split():
            # Have we seen this prefix before?
            if not prefix in elon_word_map:
                # If we haven't, add an entry to the word map
                elon_word_map[prefix] = {}
            # Have we seen this word follow the prefix?
            if word in elon_word_map[prefix]:
                # If it has, increase the count by 1
                elon_word_map[prefix][word] += 1
            else:
                # If it hasn't, set the count to 1
                elon_word_map[prefix][word] = 1

            # Add word to prefix
            prefix = prefix + (word,)
            if len(prefix) > prefix_length:
                # Remove starting word from prefix
                prefix = prefix[1:]
    return elon_word_map

def random_word(words_weight):
    if words_weight == {}:
        return None
    words = random.choices(list(words_weight.keys()), weights=list(words_weight.values()))
    return words[0]

def generate_tweet(word_map, prefix_length):
    word = random_word(word_map[tuple()])
    tweet = ""
    prefix = tuple()
    while word != None and len(tweet + word) < 280:
        tweet = tweet + word + " "
        prefix = prefix + (word,)
        if len(prefix) > prefix_length:
            prefix = prefix[1:]

        if prefix in word_map:
            # There is a word we can use
            word = random_word(word_map[prefix])
        else:
            # No words follow on from this prefix
            word = None
    if word != None:
        tweet = tweet.strip() + '...'
    return tweet.strip()

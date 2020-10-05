import random

def random_word(word_frequencies):
    if len(word_frequencies) == 0:
        return None
    words = random.choices(list(word_frequencies.keys()), weights=list(word_frequencies.values()))
    return words[0]

def create_word_map(tweets, prefix_length):
    word_map = { tuple(): {} }
    for tweet in tweets:
        prefix = tuple()
        for word in tweet.split():
            if word in word_map[prefix]:
                word_map[prefix][word] += 1
            else:
                word_map[prefix][word] = 1
            prefix = prefix + (word,)
            if len(prefix) > prefix_length:
                prefix = prefix[1:]
            if prefix not in word_map:
                word_map[prefix] = {}
    return word_map

def generate_tweet(word_map, prefix_length):
    word = random_word(word_map[tuple()])
    tweet = ""
    prefix = tuple()
    while word != None and len(tweet + word) < 280:
        tweet = tweet + word + " "

        prefix += (word,)

        if len(prefix) > prefix_length:
            prefix = prefix[1:]
        word = random_word(word_map[prefix])

    tweet = tweet.strip()
    if word != None:
        tweet += "." * (280 - len(tweet))
    return tweet

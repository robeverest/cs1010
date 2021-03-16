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


# The web app is below

from flask import Flask, request, session
from pyhtml import html, body, p, h1, form, input_

app = Flask(__name__)

app.config['SECRET_KEY'] = "correcthorsebatterystaple"

@app.route('/', methods=['POST', 'GET'])
def main_page():
    result = ""
    if not 'correct' in session:
        session['correct'] = 0
        session['total'] = 0

    if request.method == 'POST':
        if 'first_choice' in request.form:
            tweet = session['first_tweet']
        else:
            tweet = session['second_tweet']

        if tweet in elon_tweets:
            result = "Correct"
            session['correct'] = int(session['correct']) + 1
        else:
            result = "Incorrect"
        session["total"] = int(session['total']) + 1

        del session['first_tweet']
        del session['second_tweet']
    
    if 'first_tweet' in session:
        first_tweet = session['first_tweet']
        second_tweet = session['second_tweet']
    else:
        fake_tweet = None
        while fake_tweet == None or fake_tweet in elon_tweets:
            fake_tweet = generate_tweet(word_map, prefix_length)
        real_tweet = random.choice(elon_tweets)

        if random.randint(0,1) == 0:
            first_tweet = fake_tweet
            second_tweet = real_tweet
        else:
            first_tweet = real_tweet
            second_tweet = fake_tweet

    session['first_tweet'] = first_tweet
    session['second_tweet'] = second_tweet

    choice_form = form(action='/')(
        p(result),
        p(first_tweet),
        input_(type="submit", name="first_choice", value="This is the real tweet"),
        p(second_tweet),
        input_(type="submit", name="second_choice", value="This is the real tweet"),
        p(str(session['correct']) + '/' + str(session['total']) + ' tweets correctly identified')
    )

    response = html(body(
        h1("Musk or Bot"),
        choice_form
    ))
    return str(response)

if __name__ == "__main__":
    prefix_length = 2
    word_map = generate_word_map(prefix_length)
    app.run(debug=True)
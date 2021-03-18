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
from pyhtml import html, body, p, h1, form, input_, link, head, div

import csv

app = Flask(__name__)

app.config['SECRET_KEY'] = "correcthorsebatterystaple"

@app.route('/', methods=['POST', 'GET'])
def main_page():
    result = ""
    if not 'id' in session:
        session['id'] = random.randint(0,1000000000000)
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
        
        store_result(session['id'],session['first_tweet'], session['second_tweet'], tweet, result)
        
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

    header = head(
        link(rel="stylesheet", href="https://unpkg.com/purecss@2.0.5/build/pure-min.css", integrity="sha384-LTIDeidl25h2dPxrB2Ekgc9c7sEC3CWGM6HeFmuDNUjX76Ert4Z4IY714dhZHPLd", crossorigin="anonymous"),
        link(rel="stylesheet", href="static/style.css"))
    
    choice_form = form(action='/')(
        # The result of the users last choice
        p(result),
        # The first tweet
        div(class_="tweet-container")(p(first_tweet)),
        # The button to choose the first tweet
        input_(type="submit", class_="pure-button pure-button-primary", name="first_choice", value="This is the real tweet"),
        # The second tweet
        div(class_="tweet-container")(p(second_tweet)),
        # The button to choose the second tweet
        input_(type="submit", class_="pure-button pure-button-primary", name="second_choice", value="This is the real tweet"),
        # The number of tweets identified
        p(str(session['correct']) + '/' + str(session['total']) + ' tweets correctly identified')
    )

    response = html(
        header,
        body(div(class_="content")(
            h1("Musk or Bot"),
            choice_form
    )))
    return str(response)

def store_result(id, first_tweet, second_tweet, chosen_tweet, result):
    f = open('musk_or_bot.csv', 'a')
    csv_writer = csv.writer(f)
    csv_writer.writerow([id, first_tweet, second_tweet, chosen_tweet, result])
    f.close()

if __name__ == "__main__":
    prefix_length = 2
    word_map = generate_word_map(prefix_length)
    app.run(debug=True)
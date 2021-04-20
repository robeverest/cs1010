import requests
import json
from flask import Flask, request
from pyhtml import html, body, img, p

app = Flask(__name__)

@app.route('/')
def main_page():
    response = requests.get('https://aws.random.cat/meow')
    cat_picture_url = json.loads(response.content)['file']

    response = requests.get('https://cat-fact.herokuapp.com/facts/random')
    cat_fact = json.loads(response.content)['text']

    return str(html(body(
        img(src=cat_picture_url),
        p(cat_fact)
    )))

if __name__ == "__main__":
    app.run(debug=True, port=8181)


# for somthing int something_else:
#     options.append(....)
# select(options*)

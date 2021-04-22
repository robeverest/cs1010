from flask import Flask, request
from pyhtml import html, body, input_, form, p

app = Flask(__name__)

@app.route('/')
def main_page():
    text_form = form(action='/results')(
        input_(type="text", name="message"),
        input_(type="submit")
    )
    return str(html(body(text_form)))

@app.route('/results', methods=['POST'])
def results_page():
    text = request.form["message"]
    characters = len(text)
    non_punctuation = len(text) - text.count('.') - text.count(',') - text.count(' ')
    words = len(text.split())
    return str(html(body(
        p("There are " + str(characters) + " characters in the text"),
        p("There are " + str(non_punctuation) + " important characters in the text"),
        p("There are " + str(words) + " words in the text")
    )))

if __name__ == "__main__":
    app.run(debug=True, port=8181)
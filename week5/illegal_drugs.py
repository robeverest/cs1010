from flask import Flask, request
from pyhtml import html, body, h1, p, a, img, form, input_, label, head, script

app = Flask(__name__)

@app.route('/')
def survey():
    header = head(script(src="static/illegal_drugs.js"))
    example_form = form(action="thanks", name="drugs_form", onsubmit="adjust_answer();")(
        input_(type="radio", name="drugs", value="yes"),
        label(for_="yes")("Yes, I do illegal drugs"),
        input_(type="radio", name="drugs", value="no"),
        label(for_="no")("No, I don't do illegal drugs"),
        input_(type="submit"))
    response = html(
        header,
        body(
            example_form
        )
    )
    return str(response)

@app.route('/thanks', methods=["GET", "POST"])
def thanks():
    message = "Thank you for submitting " + request.form['drugs']
    return message

if __name__ == "__main__":
    app.run(debug=True)
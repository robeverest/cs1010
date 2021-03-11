from flask import Flask, request
from pyhtml import html, body, h1, p, a, img, form, input_, label

app = Flask(__name__)

@app.route('/')
def hello():
    example_form = form(action="goodbye")(
        label("Enter a message:",
            input_(type="text", name="message"),
            input_(type="submit")))
    response = html(
        body(
            h1("Welcome"), 
            p("Hello, how are you?"),
            # <a href="https://google.com">Go to google</a>
            a(href="https://google.com")("Go to google"),
            img(src="https://source.unsplash.com/J1E6XzW1INk", width=500),
            example_form
        )
    )
    return str(response)

@app.route('/goodbye', methods=["GET", "POST"])
def goodbye():
    message = request.form['message']
    return message

@app.route('/echo/<message>')
def echo(message):
    if message == "supersecretpassword":
        return "You have accessed my secret"
    else:
        return message + "!!!!"

if __name__ == "__main__":
    app.run(debug=True)
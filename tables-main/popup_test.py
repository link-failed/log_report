from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def predict():
    return render_template('popup.html')


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('a.html')


@app.route("/getimage")
def get_img():
    return "a.png"


if __name__ == '__main__':
    app.run()
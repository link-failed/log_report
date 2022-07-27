from flask import Flask, render_template
from getLogTableInfo import log_info_for_table

app = Flask(__name__)
items = log_info_for_table()


@app.route('/')
def index():
    records = items
    return render_template('query_log.html', title='Query Log',
                           records=records)


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request
from getLogTableInfo import log_info_for_table
import json
import matplotlib.pyplot as plt

app = Flask(__name__)
items = log_info_for_table()


def draw_bar_from_json(json_file, model_name):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)

        start_time = []
        duration = []
        for st in sorted(json_dict[model_name].keys()):
            start_time.append(st)
            duration.append(json_dict[model_name][st])
        print("start time: " + str(start_time))
        print("duration: " + str(duration))
        plt.barh(start_time, duration)
        plt.title(model_name)
        plt.ylabel('start time')
        plt.xlabel('duration')
        fig_name = 'static/' + model_name + '.png'
        plt.savefig(fig_name)
        plt.cla()


# TODO: delete level flag in json report
@app.route('/draw_duration')
def get_fig():
    model_name = request.args.get("node_name") + "[debug]"
    draw_bar_from_json("log_report3.json", model_name)
    return "static/" + model_name + ".png"


@app.route('/')
def index():
    records = items
    return render_template('query_log.html', title='Query Log',
                           records=records)


if __name__ == '__main__':
    app.run()

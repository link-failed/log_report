from flask import Flask, render_template, request
from get_log_table_info import log_info_for_table
from pg_stat.find_stat import get_index_info
import json
import matplotlib.pyplot as plt

app = Flask(__name__)
items = log_info_for_table()
index_info = get_index_info()


def draw_bar_from_json(json_file, model_name):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)

        start_time = []
        duration = []
        for st in sorted(json_dict[model_name].keys()):
            start_time.append(st)
            duration.append(float(json_dict[model_name][st]))

        plt.figure(figsize=(10, 6), dpi=120)
        plt.barh(start_time, duration)
        plt.title(model_name, fontweight='bold')
        plt.ylabel('start time', fontweight='bold')
        plt.xlabel('duration', fontweight='bold')

        for i, v in enumerate(duration):
            plt.text(v, i, " "+str(v), va='center')

        fig_name = 'static/' + model_name + '.png'
        plt.xticks([])
        plt.subplots_adjust(top=0.905, bottom=0.11, left=0.27, right=0.830, hspace=0.2, wspace=0.2)
        plt.savefig(fig_name)
        plt.cla()


def get_bar():
    duration_list = []
    for item in items:
        duration_list.append(float(item["duration"]))
    duration_list.sort()
    if len(duration_list) <= 4:
        # disable the top 3 longest query info
        return float('inf')
    else:
        return duration_list[-4]
# should be over that


@app.route('/draw_duration')
def get_fig():
    model_name = request.args.get("node_name")
    draw_bar_from_json("log_report4.json", model_name)
    return "static/" + model_name + ".png"


@app.route('/')
def index():
    records = items
    return render_template('query_log.html', title='Query Log', records=records, bar=get_bar())


@app.route('/index_info')
def show_index_info():
    records = index_info
    return render_template('index_info.html', title='Index Optimization', records=records)


if __name__ == '__main__':
    app.run()

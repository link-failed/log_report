import json
import matplotlib.pyplot as plt


def draw_bar_from_json(json_file):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)

        model_name = "kdigo_uo[debug]"
        start_time = []
        duration = []
        for st in sorted(json_dict[model_name].keys()):
            start_time.append(st)
            duration.append(json_dict[model_name][st])
        plt.barh(start_time, duration)
        plt.title(model_name)
        plt.ylabel('start time')
        plt.xlabel('duration')
        plt.savefig('duration_fig.png')
        # plt.show()


if __name__ == '__main__':
    draw_bar_from_json("log_report3.json")



import base64
from io import BytesIO

# from flask import Flask
# from matplotlib.figure import Figure
#
# app = Flask(__name__)


# @app.route("/")
# def hello():
#     # Generate the figure **without using pyplot**.
#     fig = Figure()
#     ax = fig.subplots()
#     ax.plot([1, 2])
#     # Save it to a temporary buffer.
#     buf = BytesIO()
#     fig.savefig(buf, format="png")
#     # Embed the result in the html output.
#     data = base64.b64encode(buf.getbuffer()).decode("ascii")
#     return f"<img src='data:image/png;base64,{data}'/>"
#
#
# if __name__ == '__main__':
#     app.run()

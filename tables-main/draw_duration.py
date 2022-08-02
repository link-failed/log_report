import json
import matplotlib.pyplot as plt


def draw_bar_from_json(json_file):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)
        for model_name in json_dict.keys():
            plt.figure()
            start_time = []
            duration = []
            for st in json_dict[model_name].keys():
                start_time.append(st)
                duration.append(json_dict[model_name][st])
            plt.barh(start_time, duration)
            plt.title(model_name)
            plt.ylabel('start time')
            plt.xlabel('duration')
            plt.show()


if __name__ == '__main__':
    draw_bar_from_json("log_report.json")

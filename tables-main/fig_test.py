import json
import matplotlib.pyplot as plt


def draw_bar_from_json(json_file):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)

        start_time = []
        duration = []
        for st in sorted(json_dict['age_histogram[debug]'].keys()):
            start_time.append(st)
            duration.append(json_dict['age_histogram[debug]'][st])
        print("start time: " + str(start_time))
        print("duration: " + str(duration))
        plt.figure(figsize=(10, 6), dpi=120)
        plt.barh(start_time, duration)
        plt.title("age_histogram[debug]", fontweight='bold')
        plt.ylabel('start time', fontweight='bold')
        plt.xlabel('duration (ms)', fontweight='bold')
        for i, v in enumerate(duration):
            plt.text(v, i, " "+str(v), va='center')
        plt.xticks([])
        plt.subplots_adjust(top=0.905, bottom=0.11, left=0.27, right=0.830, hspace=0.2, wspace=0.2)
        plt.show()


draw_bar_from_json('log_report3.json')

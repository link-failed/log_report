import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import csv
from palettable.cartocolors.sequential import agSunset_7, TealGrn_7
from palettable.lightbartlein.diverging import BlueGray_8, BrownBlue10_10

"""
    1. run tables-main/parse_txt.py to generate res/this_dbt_log.csv
    2. run gantt2.py to draw Gantt graph
"""

# 27 colors in total
color_set = agSunset_7.mpl_colors + TealGrn_7.mpl_colors + BlueGray_8.mpl_colors + BrownBlue10_10.mpl_colors[:5]
query_name_index = 0
execution_time_index = 1
start_time_index = 2
finish_time_index = 3
status_index = 4
pid_index = 5
thread_name_index = 6


def get_queries():
    query_list = []
    latest_log = "../res/this_dbt_log.csv"
    with open(latest_log, mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            start_time_str = row[start_time_index]
            finish_time_str = row[finish_time_index]
            start_time = pd.to_datetime(start_time_str, format='%Y-%m-%dT%H:%M:%S')
            finish_time = pd.to_datetime(finish_time_str, format='%Y-%m-%dT%H:%M:%S')
            query_duration = finish_time - start_time
            query_list.append({
                "query_name": row[query_name_index],
                "duration": query_duration,
                "start_time": start_time,
                "query_status": row[status_index],
                "thread_name": row[thread_name_index]
            })
    return query_list


def get_names():
    res = []
    query_list = get_queries()
    for query in query_list:
        res.append(query["query_name"])
    return res


def get_threads():
    thread_list = []
    query_list = get_queries()
    for query in query_list:
        current_thread = query["thread_name"]
        if current_thread not in thread_list:
            thread_list.append(current_thread)
    return sorted(thread_list)


name_list = get_names()


def get_color(query_name):
    color_index = name_list.index(query_name)
    return color_set[color_index]


if __name__ == '__main__':
    fig, gnt = plt.subplots()

    gnt.set_xlabel('Duration')
    gnt.set_ylabel('Threads')

    c_dict = {}

    for i in range(len(name_list)):
        c_dict[name_list[i]] = color_set[i]

    legend_elements = [Patch(facecolor=c_dict[i], label=i) for i in c_dict]
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.0005, 1), loc="upper left")
    plt.subplots_adjust(top=0.84, bottom=0.18, left=0.105, right=0.85, hspace=0.2, wspace=0.2)
    gnt.set_yticklabels(get_names())

    # Setting graph attribute
    # TODO: y labels cannot work
    gnt.grid(True)
    labels = [str(x) for x in get_threads()]
    gnt.set_yticklabels(labels)
    plt.yticks(range(len(get_threads())), get_threads())

    for i in get_queries():
        model_name = i["query_name"]
        if model_name != 'code_status' and model_name != 'echo_data':
            # print("model: " + str(i))
            gnt.broken_barh([(i["start_time"], i["duration"])], (int(i["thread_name"][7:]) * 10, 8),
                            facecolors=get_color(model_name))

    for i, v in enumerate(y):
        gnt.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')

    plt.show()

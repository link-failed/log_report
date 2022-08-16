import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import csv
import os
from palettable.cartocolors.sequential import agSunset_7, TealGrn_7

query_name_index = 0
execution_time_index = 1
start_time_index = 2
finish_time_index = 3
status_index = 4
pid_index = 5
thread_name_index = 6


def get_queries():
    query_list = []
    latest_log = "/home/ceci/Desktop/log_report/res/this_dbt_log.csv"
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
    name_list = []
    query_list = get_queries()
    for query in query_list:
        name_list.append(query["query_name"])
    return name_list


def get_threads():
    thread_list = []
    query_list = get_queries()
    for query in query_list:
        current_thread = int(query["thread_name"])
        if current_thread not in thread_list:
            thread_list.append(current_thread)
    return sorted(thread_list)


color_set = agSunset_7.mpl_colors + TealGrn_7.mpl_colors
path = "/home/ceci/Desktop/mimic-dbt/models"
all_dir_list = os.listdir(path)
dir_list = []
for d in all_dir_list:
    # delete other files or dirs
    if d[0] != '.' and d[-4:] != '.sql' and d != 'example':
        dir_list.append(d)


def get_color_map():
    """
     color_map: ['dir1': [model1, model2, model3], 'dir2': [model1, model2, ...] ...]
     index of dir = index of color
    """
    color_map = {}

    for d in dir_list:
        color_map[d] = []
        # get models inside the dir
        model_list = os.listdir(path + '/' + d)
        for model in model_list:
            # drop ".sql"
            color_map[d].append(model[:-4])

    return color_map


def get_color(query_name):
    # print(query_name)
    color_map = get_color_map()
    res = ""
    for this_dir in dir_list:
        for this_model in color_map[this_dir]:
            if this_model == query_name:
                res = this_dir
                break
    return color_set[list(color_map).index(res)]


if __name__ == '__main__':
    fig, gnt = plt.subplots()

    gnt.set_xlabel('Duration')
    gnt.set_ylabel('Threads')

    c_dict = {}
    for i in range(len(dir_list)):
        c_dict[dir_list[i]] = color_set[i]

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
            print("model: " + str(i))
            gnt.broken_barh([(i["start_time"], i["duration"])], (int(i["thread_name"]) * 10, 8),
                            facecolors=get_color(model_name))

    plt.show()

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import csv
import os
from log_parser import process_this_log
from palettable.cartocolors.sequential import agSunset_7, TealGrn_7
from palettable.lightbartlein.diverging import BlueGray_8, BrownBlue10_10
import mpld3

# 27 colors in total
color_set = agSunset_7.mpl_colors + TealGrn_7.mpl_colors + BlueGray_8.mpl_colors + BrownBlue10_10.mpl_colors[:5]

query_name_index = 0
execution_time_index = 1
start_time_index = 2
finish_time_index = 3
thread_name_index = 6


# process_this_log()


def get_queries():
    res = []
    latest_log = "res/res(3with3).csv"
    with open(latest_log, mode='r') as f:
        reader = csv.reader(f)
        start_time_list = []
        # skip first line (csv header)
        next(reader)
        for row in reader:
            start_time_str = row[start_time_index]
            finish_time_str = row[finish_time_index]
            start_time = pd.to_datetime(start_time_str, format='%Y-%m-%dT%H:%M:%S')
            start_time_list.append(start_time)
            finish_time = pd.to_datetime(finish_time_str, format='%Y-%m-%dT%H:%M:%S')
            query_duration = finish_time - start_time
            res.append({
                "query_name": row[query_name_index],
                "duration": query_duration,
                "start_time": start_time,
                "thread_name": row[thread_name_index]
            })
        first_start_time = sorted(start_time_list)[0]
        last_finish_time = res[-1]["start_time"] + res[-1]["duration"]
        for record in res:
            record["start_seconds"] = (record["start_time"] - first_start_time).total_seconds()
    return res, (last_finish_time-first_start_time).total_seconds()


thread_list = []
name_list = []
duration_list = []
query_list, whole_duration = get_queries()


def get_ku_duration():
    """
        find kdigo_uo.sql's duration
        if it is separated, the duration begins from ur_stg_1.sql and ends at kdigo_uo.sql
        if it is not, the duration begins from kdigo_uo.sql and also ends at kdigo_uo.sql
    """
    ku_start = "!"
    for q in query_list:
        if q["query_name"] == "ur_stg_1":
            ku_start = q["start_time"]
        if q["query_name"] == "kdigo_uo":
            uo_start = q["start_time"]
            uo_end = q["start_time"] + q["duration"]
    if ku_start == "!":
        return (uo_end - uo_start).total_seconds()
    else:
        return (uo_end - ku_start).total_seconds()


for query in query_list:
    name_list.append(query["query_name"])
    thread_list.append(query["thread_name"])
    duration_list.append(query["duration"])
thread_list = sorted(thread_list)

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
    if query_name[:3] == "ur3":
        query_name = "kdigo_uo"
    color_map = get_color_map()
    res = ""
    for this_dir in dir_list:
        for this_model in color_map[this_dir]:
            if this_model == query_name:
                res = this_dir
                break
    return color_set[list(color_map).index(res)]


def update_annot(coll_id, x, y):
    annot.xy = (x, y)
    text = f"{name_list[coll_id]} {duration_list[coll_id].total_seconds()} "
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.9)


print(name_list)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == gnt:
        for coll_id, broken_bar_collection in enumerate(gnt.collections):
            cont, ind = broken_bar_collection.contains(event)
            if cont:
                update_annot(coll_id, event.xdata, event.ydata)
                annot.set_visible(True)
                fig.canvas.draw_idle()
                return
    if vis:
        annot.set_visible(False)
        fig.canvas.draw_idle()


fig, gnt = plt.subplots()
gnt.set_xlabel('Duration(sec)')
gnt.set_ylabel('Threads')
c_dict = {}

for i in range(len(dir_list)):
    c_dict[dir_list[i]] = color_set[i]

legend_elements = [Patch(facecolor=c_dict[i], label=i) for i in c_dict]
plt.legend(handles=legend_elements, bbox_to_anchor=(1.0005, 1), loc="upper left")
plt.subplots_adjust(top=0.84, bottom=0.18, left=0.105, right=0.85, hspace=0.2, wspace=0.2)

gnt.set_yticks([int(thread_name[7:]) * 10 + 4 for thread_name in thread_list])
gnt.set_yticklabels(thread_list)

gnt.grid(axis='x')

for i in query_list:
    model_name = i["query_name"]
    if model_name != 'code_status' and model_name != 'echo_data':
        # print("model: " + str(i))
        gnt.broken_barh([(i["start_seconds"], i["duration"].total_seconds())], (int(i["thread_name"][7:]) * 10, 8),
                        facecolors=get_color(model_name))
    else:
        gnt.broken_barh([(i["start_seconds"], i["duration"].total_seconds())], (int(i["thread_name"][7:]) * 10, 8),
                        facecolors="white")

annot = gnt.annotate("", xy=(0, 0), xytext=(20, 30), textcoords="offset points",
                     bbox=dict(boxstyle="round", fc="yellow", ec="black", lw=1),
                     arrowprops=dict(arrowstyle="->"), fontsize=16)
annot.set_visible(False)

fig.set_figheight(10)
fig.set_figwidth(18)
fig.canvas.mpl_connect("motion_notify_event", hover)

whole_duration_text = "total duration: " + str(whole_duration)
ku_duration_text = "ku duration: " + str(get_ku_duration())
gnt.text(1, 1.005, whole_duration_text + "\n" + ku_duration_text,
         verticalalignment='bottom', horizontalalignment='right',
         transform=gnt.transAxes,
         color='blue', fontsize=14)

plt.subplots_adjust(top=0.855, bottom=0.18, left=0.095, right=0.80, hspace=0.2, wspace=0.2)
plt.show()

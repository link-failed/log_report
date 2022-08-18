import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import csv
from log_parser import process_this_log
from palettable.cartocolors.sequential import agSunset_7, TealGrn_7
from palettable.lightbartlein.diverging import BlueGray_8, BrownBlue10_10

# 27 colors in total
color_set = agSunset_7.mpl_colors + TealGrn_7.mpl_colors + BlueGray_8.mpl_colors + BrownBlue10_10.mpl_colors[:5]

query_name_index = 0
execution_time_index = 1
start_time_index = 2
finish_time_index = 3
status_index = 4
pid_index = 5
thread_name_index = 6


process_this_log()


def get_queries():
    query_list = []
    latest_log = "res.csv"
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


thread_list = []
name_list = []
duration_list = []
query_list = get_queries()
for query in query_list:
    name_list.append(query["query_name"])
    thread_list.append(query["thread_name"])
    duration_list.append(query["duration"])
thread_list = sorted(thread_list)


def get_color(query_name):
    color_index = name_list.index(query_name)
    return color_set[color_index]


def update_annot(coll_id, x, y):
    annot.xy = (x, y)
    text = f"{name_list[coll_id]} {duration_list[coll_id].total_seconds()} "
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.9)


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
gnt.set_xlabel('Duration')
gnt.set_ylabel('Threads')
c_dict = {}

for i in range(len(name_list)):
    c_dict[name_list[i]] = color_set[i]

legend_elements = [Patch(facecolor=c_dict[i], label=i) for i in c_dict]
plt.legend(handles=legend_elements, bbox_to_anchor=(1.0005, 1), loc="upper left")
plt.subplots_adjust(top=0.84, bottom=0.18, left=0.105, right=0.85, hspace=0.2, wspace=0.2)

gnt.set_yticks([int(thread_name[7:]) * 10 + 4 for thread_name in thread_list])
gnt.set_yticklabels(thread_list)

gnt.grid(True)

for i in get_queries():
    model_name = i["query_name"]
    if model_name != 'code_status' and model_name != 'echo_data':
        # print("model: " + str(i))
        gnt.broken_barh([(i["start_time"], i["duration"])], (int(i["thread_name"][7:]) * 10, 8),
                        facecolors=get_color(model_name))

annot = gnt.annotate("", xy=(0, 0), xytext=(20, 30), textcoords="offset points",
                     bbox=dict(boxstyle="round", fc="yellow", ec="b", lw=2),
                     arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()

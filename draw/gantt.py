import matplotlib.pyplot as plt
import pandas as pd
import csv

query_name_index = 0
execution_time_index = 1
start_time_index = 2
finish_time_index = 3
status_index = 4
pid_index = 5

fig, gnt = plt.subplots()

# Setting Y-axis limits
# gnt.set_ylim(0, 50)
# Setting X-axis limits
# gnt.set_xlim(0, 160)

gnt.set_xlabel('queries\' duration')
gnt.set_ylabel('queries')


# Setting ticks on y-axis
# gnt.set_yticks([15, 25, 35])

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
                "query_status": row[status_index]
            })
    return query_list


def get_names():
    name_list = []
    query_list = get_queries()
    for query in query_list:
        name_list.append(query["query_name"])
    return name_list


gnt.set_yticklabels(get_names())

# Setting graph attribute
gnt.grid(True)

lower_yaxis = 10
for i in get_queries():
    print(i["query_name"])
    if i["query_status"] == "error":
        gnt.broken_barh([(i["start_time"], i["duration"])], (lower_yaxis, 8), facecolors='tab:orange')
        lower_yaxis += 5
    elif i["query_status"] == "success":
        gnt.broken_barh([(i["start_time"], i["duration"])], (lower_yaxis, 8), facecolors='tab:blue')
        lower_yaxis += 5


plt.show()

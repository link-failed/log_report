import csv
import json

node_name_index = 0
execution_time_index = 1
start_time_index = 2
finish_time_index = 3
status_index = 4
pid_index = 5


def get_ave_durations(model_name):
    with open('log_report4.json', 'r') as f:
        recent_durations = []
        json_dict = json.load(f)
        if model_name in json_dict.keys():
            history_ts = sorted(json_dict[model_name].keys(), reverse=True)
            if len(history_ts) > 5:
                history_ts = history_ts[:5]
            for ts in history_ts:
                recent_durations.append(float(json_dict[model_name][ts]))
    if len(recent_durations) > 0:
        return sum(recent_durations)/len(recent_durations)
    else:
        return float('inf')


# find the latest log's info
def log_info_for_table():
    record_dict_list = []
    latest_log = "/home/ceci/Desktop/log_report/res/this_dbt_log.csv"
    with open(latest_log, mode='r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            if get_ave_durations(row[node_name_index])*1.20 < float(row[execution_time_index]):
                warning = True
            else:
                warning = False
            record_dict_list.append({
                "node_name": row[node_name_index],
                "duration": float(row[execution_time_index]),
                "start_time": row[start_time_index],
                "finish_time": row[finish_time_index],
                "node_status": row[status_index],
                "pid": row[pid_index],
                "info": warning
            })
        return record_dict_list


log_info_for_table()

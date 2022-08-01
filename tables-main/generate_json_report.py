import json
import csv

node_name_index = 9
level_index = 2
execution_time_index = 1
start_time_index = 11
finish_time_index = 8


# json file format:
# {'model_name': {'start_time1': 'duration', 'start_time2': 'duration', ...}, 'level': 'level'}


def generate_or_update_json():
    log_dict = []
    with open("../res/res2.csv", mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[execution_time_index] != '':
                execution_time = float(row[execution_time_index])
            else:
                execution_time = 0
            if execution_time > 0:
                log_dict.append({
                    row[node_name_index]: {row[start_time_index]: row[execution_time_index]},
                    "level": row[level_index]
                })
        return json.dumps(log_dict, sort_keys=True)


def json_test():


jsonFile = open("log_report.json", "w")
jsonFile.write(log_info_for_table())
jsonFile.close()


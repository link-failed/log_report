import json
import csv

node_name_index = 9
level_index = 2
execution_time_index = 1
start_time_index = 11
finish_time_index = 8


# json file format:
# {'model_name-level': {'start_time1': 'duration', 'start_time2': 'duration', ...}}


def generate_or_update_json():
    log_dict = {}
    with open("../res/res2.csv", mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[execution_time_index] != '':
                execution_time = float(row[execution_time_index])
            else:
                execution_time = 0
            if execution_time > 0:
                new_id = row[node_name_index] + '[' + row[level_index] + ']'
                # log_dict.append({
                #     new_id: {row[start_time_index]: row[execution_time_index]}
                # })
                log_dict[new_id] = {row[start_time_index]: row[execution_time_index]}
    log_json = json.dumps(log_dict, sort_keys=True)

    json_file = open("log_report2.json", "w")
    json_file.write(log_json)
    json_file.close()


def json_test():
    with open('log_report2.json', mode='r+') as f:
        json_object = json.load(f)
        json_object["vitals_first_day[debug]"]["new_time"] = "new_duration"
        f.seek(0)
        f.write(json.dumps(json_object))
        f.truncate()


# generate_or_update_json()
json_test()




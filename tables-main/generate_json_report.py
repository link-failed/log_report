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
    # log_dict = {}
    res_f = open("log_report2.json", "r+")
    json_dict = json.load(res_f)
    # json_file.write(log_json)
    with open("../res/res_test.csv", mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[execution_time_index] != '':
                execution_time = float(row[execution_time_index])
            else:
                execution_time = 0

            if execution_time > 0:
                new_id = row[node_name_index] + '[' + row[level_index] + ']'
                start_time = row[start_time_index]
                duration = row[execution_time_index]

                if new_id in json_dict.keys():
                    json_dict[new_id][start_time] = duration
                else:
                    json_dict[new_id] = {start_time: duration}

                res_f.seek(0)
                res_f.write(json.dumps(json_dict))
                res_f.truncate()
    # log_json = json.dumps(log_dict, sort_keys=True)
    res_f.close()


def json_test():
    with open('log_report2.json', mode='r+') as f:
        json_dict = json.load(f)
        json_dict["vitals_first_day[debug]"]["new_time"] = "new_duration"
        f.seek(0)
        f.write(json.dumps(json_dict))
        f.truncate()


def json_test2():
    with open('log_report2.json', mode='r+') as f:
        json_dict = json.load(f)
        print(type(json_dict))
        if "rrt_first_day[debug]" in json_dict.keys():
            print("in")
        else:
            print("not in")


generate_or_update_json()
# json_test()
# json_test2()
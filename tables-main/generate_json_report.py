import json
import csv
import os


node_name_index = 0
execution_time_index = 1
start_time_index = 2
log_report_name = "log_report3.json"

# json file format:
# {'model_name[level]': {'start_time1': 'duration', 'start_time2': 'duration', ...}}


def generate_or_update_json(log_filename):
    with open(log_filename, mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            with open(log_report_name, "r+") as res_f:
                if row[execution_time_index] != '':
                    execution_time = float(row[execution_time_index])
                else:
                    execution_time = 0

                if execution_time > 0:
                    node_name = row[node_name_index]
                    start_time = row[start_time_index]
                    duration = row[execution_time_index]
                    if os.stat(log_report_name).st_size > 0:
                        json_dict = json.load(res_f)
                        if node_name not in json_dict.keys():
                            json_dict[node_name] = {start_time: duration}
                        else:
                            json_dict[node_name][start_time] = duration

                    # when the log json is empty, it cannot be loaded as json file
                    else:
                        json_dict = {node_name: {start_time: duration}}

                    res_f.seek(0)
                    res_f.write(json.dumps(json_dict))
                    res_f.truncate()


if __name__ == '__main__':
    path = "/home/ceci/Desktop/log_report/res"
    log_files = os.listdir(path)

    print("searching dbt log files in directory: " + path)

    for log_file_name in log_files:
        print(log_file_name)
        log_file_name = path + '/' + log_file_name
        generate_or_update_json(log_file_name)

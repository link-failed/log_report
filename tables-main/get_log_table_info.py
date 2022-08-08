import csv

node_name_index = 0
execution_time_index = 1
start_time_index = 2
finish_time_index = 3
status_index = 4
pid_index = 5


# TODO:
# 1. generate report for all logs
#    maintain a json file listing all models and their history duration
# 2. show only current logs in front-end
#    find the latest .csv file and parse_pg from the last "running on" flag
# 3. permission issue (?)
# path for Mint OS 20: /var/log/postgresql/


# find latest log's filename
# for pg, not dbt
# def find_latest_log(log_directory):
#     filenames = next(walk(log_directory), (None, None, []))[2]  # [] if no file
#     latest_log = ""
#     for filename in filenames:
#         print("filename:" + filename)
#         if filename[-4:] == ".csv":
#             # if filename[-4:] == ".csv" and filename[:9] == "postgres-":
#             if filename > latest_log:
#                 latest_log = filename
#     return log_directory + '/' + latest_log


# find the latest log's info
def log_info_for_table():
    record_dict_list = []
    latest_log = "/home/ceci/Desktop/log_report/res/this_dbt_log.csv"
    with open(latest_log, mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            record_dict_list.append({
                "node_name": row[node_name_index],
                "duration": float(row[execution_time_index]),
                "start_time": row[start_time_index],
                "finish_time": row[finish_time_index],
                "node_status": row[status_index],
                "pid": row[pid_index]
            })
        return record_dict_list


log_info_for_table()

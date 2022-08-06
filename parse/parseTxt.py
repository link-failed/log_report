import json
import csv
import re
import math
import matplotlib.pyplot as plt


# json log format: https://docs.getdbt.com/reference/events-logging#structured-logging
# command: dbt --log-format json run


def find_node(line):
    rule = r'\"node_info\": (.*?):'
    return re.search(rule, line)


def find_node_name(line):
    rule = r'\"node_name\": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_materialized(line):
    rule = r'\"materialized\": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_node_finished(line):
    rule = r'\"node_finished_at\": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_node_path(line):
    rule = r'\"node_path\": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_node_started(line):
    rule = r'\"node_started_at\": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_node_status(line):
    rule = r'\"node_status\": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_resource_type(line):
    rule = r'"resource_type": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_rows_affected(line):
    rule = r'"rows_affected": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_execution_time(line):
    rule = r'"execution_time": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_failures(line):
    rule = r'"failures": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


def find_message(line):
    rule = r'\"message\": (.*?),'
    res = "" if re.search(rule, line) is None else re.search(rule, line).group(1)
    return str(res).replace("\"", "")


header_for_all_log = ['code', 'execution_time', 'level', 'msg', 'pid', 'thread_name', 'ts', 'materialized',
                      'node_finished_at', 'node_name', 'node_path', 'node_started_at', 'node_status', 'resource_type',
                      'rows_affected', 'failures', 'message']

header_for_this_log = ["node_name", "execution_time", "node_started_at", "node_finished_at", "node_status", "pid"]


def process_this_log():
    # find the last
    begin_flag = '"msg": "Running with dbt='
    log_path = '../logs_example/'
    log_name = 'dbt.log'
    res_path = '../res/'
    res_name = 'this_dbt_log.csv'
    with open(log_path + log_name, 'r') as f, open(res_path + res_name, 'w') as output:
        writer = csv.writer(output)

        # add header for the csv output
        writer.writerow(header_for_all_log)
        
        all_log = f.readlines()
        start_index = [x for x in range(len(all_log)) if begin_flag in all_log[x]]
        this_lines = all_log[start_index:]

        for jsonStr in this_lines:
            json_data = json.loads(jsonStr)
            execution_time = find_execution_time(jsonStr)
            if execution_time == "" or execution_time == "0":
                continue

            for k, v in json_data.items():
                if k == 'level':
                    level = v
                    if level == "debug":
                        continue
                elif k == 'pid':
                    pid = v

            rule = r'\"node_info\": {(.*?)},'
            if re.search(rule, jsonStr) is not None:
                record = re.search(rule, jsonStr).group(1)

                node_finished_at = find_node_finished(record)
                node_name = find_node_name(record)
                node_started_at = find_node_started(record)
                node_status = find_node_status(record)

                this_row = [node_name, execution_time, node_started_at, node_finished_at, node_status, pid]

            else:
                continue
            writer.writerow(this_row)


def process_all_log():
    log_path = '../logs_example/'
    log_name = 'dbt.log'
    res_path = '../res/'
    res_name = 'all_dbt_log.csv'
    with open(log_path + log_name, 'r') as f, open(res_path + res_name, 'w') as output:
        writer = csv.writer(output)

        # add header_for_all_log for the csv output
        writer.writerow(header_for_all_log)

        for jsonStr in f.readlines():
            json_data = json.loads(jsonStr)
            for k, v in json_data.items():
                if k == 'code':
                    code = v
                # elif k == 'data':
                #     data = v
                # elif k == 'invocation_id':
                #     invocation_id = v
                elif k == 'execution_time':
                    execution_time = v
                elif k == 'level':
                    level = v
                elif k == 'msg':
                    msg = v
                elif k == 'pid':
                    pid = v
                elif k == 'thread_name':
                    thread_name = v
                elif k == 'ts':
                    ts = v

            execution_time = find_execution_time(jsonStr)

            rule = r'\"node_info\": {(.*?)},'
            if re.search(rule, jsonStr) is not None:
                record = re.search(rule, jsonStr).group(1)

                materialized = find_materialized(record)
                node_finished_at = find_node_finished(record)
                node_name = find_node_name(record)
                node_path = find_node_path(record)
                node_started_at = find_node_started(record)
                node_status = find_node_status(record)
                resource_type = find_resource_type(record)
                rows_affected = find_rows_affected(record)
                failures = find_failures(record)
                message = find_message(record)

                this_row = [code, execution_time, level, msg, pid, thread_name, ts, materialized,
                            node_finished_at, node_name, node_path, node_started_at, node_status, resource_type,
                            rows_affected, failures, message]

            else:
                this_row = [code, execution_time, level, msg, pid, thread_name, ts]
            writer.writerow(this_row)


def main():
    process_all_log()
    process_this_log()


if __name__ == "__main__":
    main()

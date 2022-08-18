import json
import csv
import re


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


csv_header = ["node_name", "execution_time", "node_started_at", "node_finished_at", "node_status", "dbt_pid",
              "thread_name"]


def process_this_log():
    # find the last
    begin_flag = '"msg": "Running with dbt='
    log_name = 'dbt.log'
    res_name = 'res.csv'
    with open(log_name, 'r') as f, open(res_name, 'w') as output:
        writer = csv.writer(output)

        # add header for the csv output
        writer.writerow(csv_header)
        
        all_log = f.readlines()
        start_index = [x for x in range(len(all_log)) if begin_flag in all_log[x]]
        if not start_index:
            this_lines = all_log
        else:
            this_lines = all_log[start_index[-1]:]

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
                    dbt_pid = v
                elif k == 'thread_name':
                    thread_name = v
                    # thread_name = int(v[7:])

            rule = r'\"node_info\": {(.*?)},'
            if re.search(rule, jsonStr) is not None:
                record = re.search(rule, jsonStr).group(1)

                node_status = find_node_status(record)
                if node_status == 'compiling':
                    continue

                node_finished_at = find_node_finished(record)
                node_name = find_node_name(record)
                node_started_at = find_node_started(record)

                this_row = [node_name, execution_time, node_started_at, node_finished_at, node_status, dbt_pid,
                            thread_name]

            else:
                continue

            writer.writerow(this_row)


def main():
    process_this_log()


if __name__ == "__main__":
    main()

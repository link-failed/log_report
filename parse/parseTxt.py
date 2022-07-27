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


header = ['code', 'execution_time', 'level', 'msg', 'pid', 'thread_name', 'ts', 'materialized', \
          'node_finished_at', 'node_name', 'node_path', 'node_started_at', 'node_status', 'resource_type', \
          'rows_affected', 'failures', 'message']


def process_log():
    with open('../logs_example/dbt-18.log', 'r') as f, open('../res/res1.csv', 'w') as output:
        writer = csv.writer(output)

        # add header for the csv output
        writer.writerow(header)

        for jsonStr in f.readlines():
            jsonData = json.loads(jsonStr)
            for k, v in jsonData.items():
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

                prev_row = [code, execution_time, level, msg, pid, thread_name, ts, materialized,
                            node_finished_at, node_name, node_path, node_started_at, node_status, resource_type,
                            rows_affected, failures, message]

            else:
                prev_row = [code, execution_time, level, msg, pid, thread_name, ts]
            writer.writerow(prev_row)


bar_num = 40
ts_list = []
duration_list = []


def get_duration():
    # if duration_time is not null and > 0
    # id format: node_name[level]
    with open('../res/res1.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['execution_time'] != "" and float(row['execution_time']) > 0:
                duration_list.append(float(row['execution_time']))
                cut_time_index1 = row['ts'].find(':') + 1
                cut_time_index2 = row['ts'].find('.') + 3
                ts_list.append(row['ts'][cut_time_index1:cut_time_index2])


def split_list(x_list, y_list):
    group = math.ceil(len(x_list) / bar_num)
    x_list_list = []
    y_list_list = []
    index1 = 0
    index2 = bar_num
    for i in range(group):
        x_list_list.append(x_list[index1:index2])
        y_list_list.append(y_list[index1:index2])
        index1 += bar_num
        index2 += bar_num
    return group, x_list_list, y_list_list


def duration_plt():
    group, x_list_list, y_list_list = split_list(ts_list, duration_list)
    column = 2
    row = math.ceil(group / column)  # todo
    fig, axs = plt.subplots(nrows=row, ncols=column, sharey=True)  # bar_num in one time
    fig.suptitle('duration')

    i = 0
    for row in axs:
        for col in row:
            col.bar(x_list_list[i], y_list_list[i])
            i += 1
            col.tick_params(axis='x', rotation=90)

    # plt.xticks(rotation=90)
    plt.show()


def main():
    process_log()
    get_duration()
    duration_plt()


if __name__ == "__main__":
    main()

# "completed_at": "2022-07-18T00:10:04.442487Z"
# "started_at": "2022-07-18T00:10:04.4bar_numbar_num3Z"
# "node_finished_at": "2022-07-18T00:10:05.324930"
# "node_started_at": "2022-07-18T00:10:04.437969"
# "ts": "2022-07-18T00:10:05.325107Z"
# "execution_time": 0.8839113712310791 ~ node_finished-node_started?
# "created_at": 1657876846.6253757

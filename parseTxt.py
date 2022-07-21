import json
import csv
import re
import matplotlib
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
    with open('logs_example/dbt-18.log', 'r') as f, open('res/res1.csv', 'w') as output:
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

            # writer.writerow(
            #     {'code': code, 'data': data, 'invocation_id': invocation_id, 'level': level, 'msg': msg, 'pid': pid,
            #      'thread_name': thread_name, 'ts': ts, 'materialized': materialized, 'node_finished_at': node_finished_at,
            #      'node_name': node_name, 'node_path': node_path, 'node_started_at': node_started_at,
            #      'node_status': node_status, 'resource_type': resource_type, 'rows_affected': rows_affected,
            #      'execution_time': execution_time, 'failures': failures, 'message': message})

            # else:
            #     writer.writerow(
            #         {'code': code, 'data': data, 'invocation_id': invocation_id, 'level': level, 'msg': msg, 'pid': pid, \
            #          'thread_name': thread_name, 'ts': ts})


id_list = []
duration_list = []


def get_duration():
    # if duration_time is not null and > 0
    # id format: node_name[level]
    with open('res/res1.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['execution_time'] != "" and float(row['execution_time']) > 0:
                duration_list.append(float(row['execution_time']))
                id_list.append(row['node_name'] + '[' + row['level'] + ']')


def duration_plt():
    fig, ax = plt.subplots()
    b = ax.barh(range(len(id_list)), duration_list, color='#6699CC')

    # add text label
    for rect in b:
        w = rect.get_width()
        ax.text(w, rect.get_y() + rect.get_height() / 2, '%f' %
                int(w), ha='left', va='center')

    ax.set_yticks(range(len(id_list)))
    ax.set_yticklabels(id_list)

    # plt.xticks(())

    plt.title('duration', loc='center', fontsize='25', fontweight='bold')

    plt.show()


def main():
    process_log()
    get_duration()
    duration_plt()


if __name__ == "__main__":
    main()


# "completed_at": "2022-07-18T00:10:04.442487Z"
# "started_at": "2022-07-18T00:10:04.440403Z"
# "node_finished_at": "2022-07-18T00:10:05.324930"
# "node_started_at": "2022-07-18T00:10:04.437969"
# "ts": "2022-07-18T00:10:05.325107Z"
# "execution_time": 0.8839113712310791 ~ node_finished-node_started?
# "created_at": 1657876846.6253757

import csv


node_name_index = 9
level_index = 2
execution_time_index = 1
start_time_index = 11
pid_index = 4


def log_info_for_table():
    record_dict_list = []
    with open('../res/res1.csv', mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[execution_time_index] != '':
                execution_time = float(row[execution_time_index])
            else:
                execution_time = 0

            if execution_time > 0:
                record_dict_list.append({
                    "node_name": row[node_name_index],
                    "level": row[level_index],
                    "execution_time": row[execution_time_index],
                    "start_time": row[start_time_index],
                    "pid": row[pid_index]
                })
        return record_dict_list
        # for i in node_index_list:
        #     record_dict_list.append(row[i] for row in reader)


log_info_for_table()

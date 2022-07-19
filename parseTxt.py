import json
import csv
import re

# json log format: https://docs.getdbt.com/reference/events-logging#structured-logging
# command: dbt --log-format json run

count = 0
data_file = open('json_output.csv', 'w', newline='')
csv_writer = csv.writer(data_file)

# add header for csv output file

def find_sql():


with open('logs_example/dbt-18.log', 'r') as f:
    for jsonStr in f.readlines():
        jsonData = json.loads(jsonStr)
        for record in jsonData:
            if record.key() == 'code':
                code = record.value()
            elif record.key() == 'data':
                data = record.value
            elif record.key() == 'invocation_id':
                invocation_id = record.value
            elif record.key() == 'msg':
                msg = record.value
            elif record.key() == 'pid':
                pid = record.value
            elif record.key() == 'thread_name':
                thread_name = record.value
            elif record.key() == 'ts':
                ts = record.value


            csv_writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
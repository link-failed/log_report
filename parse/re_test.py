import re


def find_node_finished(line):
    # rule = r'"node_finished_at": (.*?), '
    rule = r'\"start\"(.*?)\"end\"'
    return re.findall(rule, line)


line = "{\"code\": \"Q023\", \"data\": {\"node_info\": {\"materialized\": \"table\", \"node_finished_at\": null, " \
       "\"node_name\": \"abx_prescriptions_list\", \"node_path\": \"treatment/abx_prescriptions_list.sql\", " \
       "\"node_started_at\": \"2022-07-18T00:09:27.426725\", \"node_status\": \"started\", \"resource_type\": " \
       "\"model\", \"unique_id\": \"model.mimic.abx_prescriptions_list\"}, \"unique_id\": " \
       "\"model.mimic.abx_prescriptions_list\"}, \"invocation_id\": \"7c4c3ecd-5c14-4600-9281-0e21ba30ba00\", " \
       "\"level\": \"debug\", \"log_version\": 2, \"msg\": \"Began running node model.mimic.abx_prescriptions_list\", " \
       "\"pid\": 109348, \"thread_name\": \"Thread-1\", \"ts\": \"2022-07-18T00:09:27.426805Z\", \"type\": " \
       "\"log_line\"} "

line = "\"start\"...\"end\""

print(find_node_finished(line))

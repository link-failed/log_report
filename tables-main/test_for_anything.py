# import os
#
# path = "/home/ceci/Desktop/log_report/res"
# dir_list = os.listdir(path)
#
# print("Files and directories in '", path, "' :")
#
# print(dir_list)


import json

with open("log_report.json", 'r+') as res_f:
    json_dict = json.load(res_f)
    print(json_dict)
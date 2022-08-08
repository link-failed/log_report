# import os
#
# path = "../logs_example/"
# dir_list = os.listdir(path)
#
# print("Files and directories in '", path, "' :")
#
# for f in dir_list:
#     if f[-4:] == '.log':
#         print(f)


# import json
#
# with open("log_report.json", 'r+') as res_f:
#     json_dict = json.load(res_f)
#     print(json_dict)


duration_list = [1, 3, 5, 2, 4, 6]
duration_list.sort()
print(duration_list)
print(duration_list[-3])

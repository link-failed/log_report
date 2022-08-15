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


from palettable.cartocolors.sequential import agSunset_7, TealGrn_7
color_set = agSunset_7.mpl_colors + TealGrn_7.mpl_colors
print(len(color_set))

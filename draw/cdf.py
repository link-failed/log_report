import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

start_time_index = 2
finish_time_index = 3


def get_sec_list():
    start_time_list = []
    finish_time_list = []
    latest_log = "/home/ceci/Desktop/log_report/res/this_dbt_log.csv"
    with open(latest_log, mode='r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            start_time = pd.to_datetime(row[start_time_index], format='%Y-%m-%dT%H:%M:%S')
            finish_time = pd.to_datetime(row[finish_time_index], format='%Y-%m-%dT%H:%M:%S')
            start_time_list.append(start_time)
            finish_time_list.append(finish_time)
    start = sorted(start_time_list)[0]
    sec_list = [(time-start).total_seconds() for time in finish_time_list]
    return sec_list


if __name__ == '__main__':
    x = get_sec_list()
    frequency = [1] * len(x)
    pdf = frequency/np.sum(frequency)
    cdf = np.cumsum(pdf)
    print(x)
    print(cdf)

    plt.plot(x, cdf, marker="o", label="with 5 threads")
    # plt.plot(x, cdf, marker="o", label="CDF")
    plt.ylim(0, 1.15)
    plt.xlabel("duration(sec)")
    plt.title("cdf for queries")
    plt.legend()
    plt.show()

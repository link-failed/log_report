# log_report_generation

## from dbt log (json)


json log format: https://docs.getdbt.com/reference/events-logging#structured-logging
command: dbt --log-format json run

process:
 1. dbt.log -> [parse_txt.py] -> this_dbt_log.csv
    dbt.log -> [parse_txt.py] -> all_dbt_log.csv
 2. this_dbt_log.csv -> [parse_txt.py] -> [generate_json_report.py] -> log_report.json
    log_report.json -> [basic_table.py] -> Flask front-end
 3. (click button to show history duration figure)
    this_dbt_log.csv -> [[basic_table.py]] -> bar chart

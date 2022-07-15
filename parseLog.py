import pandas as pd

# csvlog format:
# https://www.postgresql.org/docs/9.6/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-CSVLOG

file = pd.read_csv('postgresql-2022-07-15_172235.csv', quotechar='"', sep=",")
file.columns = ["log_time", "user_name", "database_name", "process_id", "connection_from", "session_id", \
                "session_line_num", "command_tag", "session_start_time", "virtual_transaction_id", \
                "transaction_id", "error_severity", "sql_state_code", "message", "detail", "hint", \
                "internal_query", "internal_query_pos", "context", "query", "query_pos", "location", \
                "application_name"]

# test
print(file[['application_name']])
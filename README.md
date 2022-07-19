# log_report_generation

## from dbt log (json)

reference: https://docs.getdbt.com/reference/events-logging#structured-logging

| Field                                                        | Description                                                  | example | involved |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------- | -------- |
| `code`                                                       | A unique identifier for each event type                      |         |          |
| `data`                                                       | A dictionary containing programmatically accessible information about the log line. The contents of this dictionary vary based on the event type which generated this log message. |         | y        |
| [`invocation_id`](https://docs.getdbt.com/reference/dbt-jinja-functions/invocation_id) | A unique identifier for this invocation of dbt               |         |          |
| `level`                                                      | A string representation of the log level (`debug`, `info`, `warn`, `error`) |         | y        |
| `log_version`                                                | Integer indicating version                                   |         |          |
| `msg`                                                        | The human-friendly log message. **Note**: This message is not intended for machine consumption. Log messages are bject to change in future versions of dbt, and those changes may or may not coincide with a change in `log_version`. |         | y        |
| `node_info`                                                  | If applicable, a dictionary of human- and machine-friendly information about a currently running resource |         | y        |
| `pid`                                                        | The process ID for the running dbt invocation which produced this log message |         | y        |
| `thread_name`                                                | The thread in which the log message was produced, helpful for tracking queries when dbt is run with ltiple threads |         | y        |
| `ts`                                                         | When the log line was printed                                |         | y        |
| `type`                                                       | Always `log_line`                                            |         |          |

| node_info Field    | Description                                                  | example | involved |
| ------------------ | ------------------------------------------------------------ | ------- | -------- |
| `materialized`     | view, table, incremental, etc.                               |         | y        |
| `node_finished_at` | Timestamp when node processing completed                     |         | y        |
| `node_name`        | Name of this model/seed/test/etc                             |         | y        |
| `node_path`        | File path to where this resource is defined                  |         | y        |
| `node_started_at`  | Timestamp when node processing started                       |         | y        |
| `node_status`      | Current status of the node, as defined in [the result contract](https://github.com/dbt-labs/dbt-core/blob/HEAD/core/dbt/contracts/results.py#L61-L74) |         | y        |
| `resource_type`    | model, test, seed, snapshot, etc.                            |         | y        |
| `type`             | Always `'node_status'`                                       |         | y        |
| `unique_id`        | The unique identifier for this resource, which can be used to look up contextual information in a [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json) |         | y        |

## from pg log (csv)

reference: https://www.postgresql.org/docs/current/runtime-config-logging.html#RUNTIME-CONFIG-LOGGING-CSVLOG

```
PRIMARY KEY (session_id, session_line_num)
```

| Field                  | Description                 | example                                    | involved |
| ---------------------- | --------------------------- | ------------------------------------------ | -------- |
| log_time               | timestamp(3) with time zone | 2022-07-18 08:18:02.436 CST                | y        |
| user_name              | \                           | \                                          | y        |
| database_name          | \                           | \                                          | y        |
| process_id             |                             | 110054                                     | y        |
| connection_from        |                             | 127.0.0.1:55248                            | y        |
| session_id             |                             | 62d4a538.1ade6                             | y        |
| session_line_num       |                             | 1                                          |          |
| command_tag            |                             | BEGIN                                      |          |
| session_start_time     | timestamp with time zone    | 2022-07-18 08:18:11 CST                    | y        |
| virtual_transaction_id | text                        | 3/10443                                    |          |
| transaction_id         | bigint                      | 0                                          |          |
| error_severity         |                             | WARNING / LOG / ERROR                      | y        |
| sql_state_code         |                             | 25001                                      |          |
| message                |                             | there is already a transaction in progress |          |
| detail                 |                             | hasn't appeared yet                        | ?        |
| hint                   |                             | hasn't appeared yet                        | ?        |
| internal_query         |                             | hasn't appeared yet                        | ?        |
| internal_query_pos     |                             | hasn't appeared yet                        | ?        |
| context                |                             | hasn't appeared yet                        | ?        |
| query                  |                             | with sql                                   | y        |
| query_pos              |                             | 5340                                       |          |
| location               |                             | hasn't appeared yet                        | ?        |
| application_name       |                             | dbt                                        |          |

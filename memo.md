# other tools

## 1. dbt_log_parser

generate Json report:

```json
{
    "models_found": 469,
    "tests_found": 1658,
    "snapshots_found": 0,
    "analyses_found": 0,
    "macros_found": 300,
    "operations_found": 0,
    "seeds_found": 0,
    "sources_found": 204,
    "tests_run": 1100,
    "tests_runtime_seconds": 97.47,
    "tests": [
        {
            "number": 1,
            "name": "accepted_values_dim_order_state_open",
            "status": "PASS",
            "total_time": 2.11
        },
        {
            "status": "WARN",
            "number": 2,
            "name": "relationships_fact_contribution_goal_updates_contribution_page_id__contribution_page_id__ref_dim_contribution_page_",
            "total_time": 1.73,
            "query_results": {
                "found": 5,
                "expected": 0
            },
            "query": {
                "filepath": "target/compiled/core/schema_test/relationships_fact_contribution_goal_updates_34dae512835158ed459182c173a8c127.sql",
                "sql": null,
                "file_err": true
            }
        }
    ]
}
```



## 2. pg_qualstats

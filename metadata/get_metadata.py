from moz_sql_parser import parse
import json


def parse_and_display(query):
    parsed = parse(query)
    json_output = json.dumps(parsed, indent=2)
    print("output json - {}".format(json_output))


if __name__ == "__main__":
    text_file = open("test.sql", "r")
    sql_file = text_file.read()
    text_file.close()

    parse_and_display(sql_file)

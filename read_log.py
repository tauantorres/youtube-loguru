import pandas as pd
import json
from IPython.display import display

file_path = "app.log"

def read_log(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines

def parse_log_lines(lines):
    parsed_lines = [json.loads(line) for line in lines]
    return parsed_lines

def expand_records(data):
    expanded_data = []
    for entry in data:
        record = entry['record']
        text = json.loads(entry['text'])
        flattened_record = {
            **text,
            **record,
            'record_elapsed': record['elapsed']['repr'],
            'record_time': record['time']['repr'],
            'record_level': record['level']['name'],
            'record_message': record['message'],
            'record_function': record['function'],
            'record_file': record['file']['name'],
            'record_line': record['line'],
            'record_module': record['module'],
            'record_process_id': record['process']['id'],
            'record_thread_id': record['thread']['id']
        }
        expanded_data.append(flattened_record)
    return expanded_data

def create_dataframe(data):
    df = pd.DataFrame(data)
    return df

def main():
    lines = read_log(file_path)
    data = parse_log_lines(lines)
    expanded_data = expand_records(data)
    df = create_dataframe(expanded_data)
    display(df)

if __name__ == "__main__":
    main()

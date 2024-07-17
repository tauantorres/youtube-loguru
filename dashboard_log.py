import dash
from dash import dcc, html, dash_table
import pandas as pd
import json

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
        # Ensure all values are strings, numbers, or booleans
        for key, value in flattened_record.items():
            if not isinstance(value, (str, int, float, bool)):
                flattened_record[key] = str(value)
        expanded_data.append(flattened_record)
    return expanded_data

def create_dataframe(data):
    df = pd.DataFrame(data)
    return df

lines = read_log(file_path)
data = parse_log_lines(lines)
expanded_data = expand_records(data)
df = create_dataframe(expanded_data)

# Create a Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Log Dashboard"),
    dash_table.DataTable(
        id='log-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={
            'height': 'auto',
            'minWidth': '0px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        },
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

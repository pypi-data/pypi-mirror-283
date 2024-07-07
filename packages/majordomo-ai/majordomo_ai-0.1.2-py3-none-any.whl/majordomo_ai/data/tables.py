import requests
import os
import json
from pathlib import Path

def create_table_from_csv(connection, 
                          data_source, 
                          sql_database,
                          table_name,
                          **kwargs
                          ):
    debug_on = False

    json_input = {}
    azure_credentials = {}
    azure_blob = {}

    json_input['sql_database'] = sql_database
    json_input['table_name'] = table_name
    json_input['input_file'] = data_source['input_file']

    # Fill the default values.
    json_input['append'] = False

    # Parse the user overrides.
    for key, value in kwargs.items():
        match key:
            case "debug_on":
                debug_on = value
            case "append":
                append = value
            case default:
                pass

    json_input['data_source'] = data_source['source']
    del data_source['source']

    match json_input['data_source']:

        case "azure_blob":
            json_input['azure_blob'] = data_source

        case "aws_s3":
            json_input['aws_s3'] = data_source

        case "local":
            json_input['input_file'] = os.path.basename(data_source['input_file'])
            my_file = Path(data_source['input_file'])
            if not my_file.is_file():
                raise ValueError("Input file not found")

            file = {'file': open(data_source['input_file'], 'rb')}

            resp  = requests.post(connection['client_url'] + '/file_upload', files=file)
            if debug_on:
                print(resp.json())

        case "webpage":
            json_input['input_file'] = data_source['input_file']

        case default:
           pass

    try:
        headers = {"Content-Type": "application/json"}
        json_data = json.dumps(json_input)
        result = requests.post(connection['client_url'] + '/csv_ingestion', data=json_data, headers=headers)
        if debug_on:
            print(result.content)
    except Exception as e: raise

    return result

def sql_tables_query(connection, 
                 embedding_model, 
                 llm_model, 
                 database, 
                 table_names, 
                 query_str,
                 **kwargs
                 ):
    debug_on = False

    json_input = {}

    json_input['user_token'] = connection['user_token']

    # Fill the default values.
    json_input['embedding_model'] = embedding_model
    json_input['llm_model'] = llm_model
    json_input['database'] = database
    json_input['table_names'] = table_names
    json_input['query'] = query_str

    # Parse the user overrides.
    for key, value in kwargs.items():
        match key:
            case "debug_on":
                debug_on = value
            case default:
                pass

    try:
        headers = {"Content-Type": "application/json"}
        json_data = json.dumps(json_input)
        result = requests.post(connection['client_url'] + '/sql_query', data=json_data, headers=headers)
        if debug_on:
            print(result.content)
    except Exception as e: raise

    return result

#create_table_from_csv("http://127.0.0.1:8000",
#                      "stock",
#                      "table1",
#                      "local",
#                      "/home/azureuser/Stock Price.csv",
#                      debug_on=True
#                      )
#
#tables = ["table1"]
#tables_query("http://127.0.0.1:8000",
#          "md-02c52fd6-a17c-4169-aebb-1cb4fa7ee60c", 
#          "text-embedding-3-large",
#          "gpt-3.5-turbo",
#          "stock",
#          tables,
#          "Which is the best performing stock in last 3 months in percentage terms?"
#          )

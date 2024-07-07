import requests
from pathlib import Path
import os
import json
from datetime import datetime

def create_dataset_from_documents(connection, dataset, data_source, **kwargs):

    debug_on = False

    json_input = {}

    json_input['dataset'] = dataset

    json_input['user_token'] = connection['user_token']

    json_input['pdf_extractor'] = "PyMuPDF"

    json_input['data_source'] = data_source['source']
    del data_source['source']

    match json_input['data_source']:

        case "azure_blob":
            json_input['azure_blob'] = data_source

        case "aws_s3":
            json_input['aws_s3'] = data_source

        case "slack":
            json_input['slack_channel'] = data_source

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

    # Parse the user overrides.
    for key, value in kwargs.items():
        match key:
            case "debug_on":
                debug_on = value
            case "pdf_extractor":
                json_input['pdf_extractor'] = value
            case default:
                pass

    try:
        headers = {"Content-Type": "application/json"}
        json_data = json.dumps(json_input)
        result = requests.post(connection['client_url'] + '/doc_ingestion', data=json_data, headers=headers)
        if debug_on:
            print(result.content)
    except Exception as e: raise

    return result

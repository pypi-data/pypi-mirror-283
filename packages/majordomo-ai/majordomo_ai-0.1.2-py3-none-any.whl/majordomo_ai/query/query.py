import requests
from pathlib import Path
import os
import json

def llm_query(connection, 
              dataset, 
              embedding_model, 
              llm_model, 
              query_str,
              **kwargs
              ):
    debug_on = False

    json_input = {}

    json_input['user_token'] = connection['user_token']

    # Fill the default values.
    json_input['dataset'] = dataset
    json_input['embedding_model'] = embedding_model
    json_input['llm_model'] = llm_model
    json_input['dataset'] = dataset
    json_input['query'] = query_str
    json_input['temperature'] = 1.0
    json_input['top_k'] = 2

    # Parse the user overrides.
    for key, value in kwargs.items():
        match key:
            case "debug_on":
                debug_on = value
            case "temperature":
                json_input['temperature'] = value
            case "top_k":
                json_input['top_k'] = value
            case default:
                pass

    try:
        headers = {"Content-Type": "application/json"}
        json_data = json.dumps(json_input)
        result = requests.post(connection['client_url'] + '/doc_query', data=json_data, headers=headers)
        if debug_on:
            print(result.content)
    except Exception as e: raise

    return result

#llm_query("http://127.0.0.1:8000",
#          "md-02c52fd6-a17c-4169-aebb-1cb4fa7ee60c", 
#          "text-embedding-3-large",
#          "gpt-3.5-turbo",
#          "test",
#          "What is special about the case?"
#          )

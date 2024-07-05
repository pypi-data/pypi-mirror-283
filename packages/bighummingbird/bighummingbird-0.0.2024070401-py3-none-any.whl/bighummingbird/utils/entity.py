import requests
import json
import inspect
from .constants import MODEL_BASE_URL
from .file import upload_data, get_data_size
from .source_code import get_source_code_hash

def _get_model_tag(name, hash, projectId, api_key):
    model_tag_response = requests.post(MODEL_BASE_URL + "/tag", json={
        'name': name,
        'hash': hash,
        'projectId': projectId,
    }, headers={'Authorization': f'Bearer {api_key}'})

    if model_tag_response.status_code != 200:
        raise ValueError("Failed to get model tag")

    model_tag_response_body = json.loads(model_tag_response.text)
    model_tag = model_tag_response_body["tag"]
    model_version = model_tag_response_body["version"]
    model_exists_previously = model_tag_response_body["exists"]
    return model_tag, model_version, model_exists_previously

def _upload_model_code(api_key, hash, name, projectId, source_code):
    model_tag, model_version, model_exists_previously = _get_model_tag(name, hash, projectId, api_key)
    model_filename = projectId + "_" + model_tag + ".txt"
    if not model_exists_previously:
        upload_data(model_filename, source_code, api_key)
    return model_tag, model_version, model_filename

def create_model(name, source_code, inputs, outputs, projectId, api_key):
    code, hash_digest, model_name = get_source_code_hash(source_code)
    
    model_tag, model_version, model_filename = _upload_model_code(
        api_key=api_key,
        hash=hash_digest,
        name=name,
        projectId=projectId,
        source_code=code,
    )

    data_size = get_data_size(code)
    model_response = requests.post(MODEL_BASE_URL, json={
        'codeFilename': model_filename,
        'dataSize': data_size,
        'hash': hash_digest,
        'inputs': inputs,
        'modelTag': model_tag,
        "name": model_name,
        'outputs': outputs,
        'projectId': projectId,
        'version': model_version,
    }, headers={'Authorization': f'Bearer {api_key}'})

    if model_response.status_code != 201:
        raise ValueError("Failed to create or fetch model with model tag: " + model_tag)

    return model_tag

def get_input_types(func):
    signature = inspect.signature(func)
    param_types = []
    
    for (param_name, param) in signature.parameters.items():
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
        param_types.append({'name': param_name, 'type': param_type.__name__.lower()})
    
    return param_types
 

def get_type(input):
    if isinstance(input, dict):
        return {key: get_type(value) for key, value in input.items()}
    elif isinstance(input, list):
        return [get_type(item) for item in input]
    else:
        return type(input).__name__


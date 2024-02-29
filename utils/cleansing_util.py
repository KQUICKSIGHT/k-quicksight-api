import os
import uuid
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from AutoClean import AutoClean
import ast
import numpy as np

import pandas as pd

dotenv_path_dev = '.env.development'
load_dotenv(dotenv_path=dotenv_path_dev)

file_server_path_file = os.getenv("FILE_SERVER_PATH_FILE")
file_base_url = os.getenv("BASE_URL_FILE")

ALLOWED_EXTENSIONS_FILE = ['.csv', '.json', '.txt', '.xlsx']


def get_file_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension


def handle_uploaded_file_cleansing(f):

    extension = get_file_extension(f.name)

    filename = str(uuid.uuid4().hex) + extension

    file_size = f.size

    with open(file_server_path_file + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return {"filename": filename, "size": str(file_size), "type": extension.replace('.', ''), "location": file_server_path_file+filename}


def find_inncurate_file(f):

    extension = get_file_extension(f.name)
    result = None
    if extension == ".csv":
        result = clean_csv(f)
    elif extension == ".json":
        result = clean_json(f)
    elif extension == ".txt":
        resuult = clean_txt(f)
    elif extension == ".xlsx":
        result = clean_xlsx(f)

    return result


def clean_csv(f):
    data = pd.read_csv(f)

    duplicate_rows = data[data.duplicated(keep=False)]
    missing_values = data[data.isna().any(axis=1)]
    missing_values.replace([np.inf, -np.inf], np.nan, inplace=True)

    return missing_values


def clean_json(f):

    pass


def clean_txt(f):

    pass


def clean_xlsx(f):

    pass

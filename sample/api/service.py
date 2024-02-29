# prepare put in shellscripts


import os
import uuid
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import chardet
import utils.file_util as util
from rest_framework import status
import csv
import subprocess
import json
import os
import utils.file_util as file_utile
from django.http import HttpResponse

dotenv_path_dev = '.env'
load_dotenv(dotenv_path=dotenv_path_dev)

file_server_path_file = os.getenv("FILE_SERVER_PATH_FILE")
file_base_url = os.getenv("BASE_URL_FILE")


def get_delimiter(file_path, num_lines=5):
    try:
        with open(file_path, 'r', newline='') as file:
            # Read a few lines from the text file for analysis
            sample_lines = [file.readline() for _ in range(num_lines)]

            # Use the Sniffer class to detect the delimiter
            dialect = csv.Sniffer().sniff(''.join(sample_lines))

            # The delimiter is stored in the 'delimiter' attribute of the dialect
            return dialect.delimiter
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




def get_file_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension


def detect_delimiter(file_path):
    with open(file_path, 'r') as file:
        sample = file.read(1024)  # Read a sample of the file
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter


def load_dataset(filename, size=0,file=None):

    file_path = file_server_path_file+filename
    type_file = get_file_extension(filename).replace('.', "").strip()
    data = None

    try:

        with open(file_path, 'rb') as raw_data:
            result = chardet.detect(raw_data.read(1000))
        encoding = result['encoding']

        if type_file == 'csv':
            try:
                data = pd.read_csv(file_path, encoding=encoding,
                                   on_bad_lines="skip")
            except UnicodeDecodeError:
                data = pd.read_csv(file_path, encoding="latin1",
                                   on_bad_lines="skip")

        elif type_file == 'json':

            try:
                data = pd.read_json(file_path, encoding=encoding)

            except Exception as e:

                print(e)
        elif type_file == 'txt':

            data = pd.read_csv(file_path, encoding=encoding,
                               delimiter=detect_delimiter(file_path))
        elif type_file == 'xlsx':

            data = pd.read_excel(file_path)

    except FileNotFoundError as e:

        print(e)

    if data is not None and not data.empty:

        data = data.where(pd.notnull(data), None)
        data = data.apply(lambda x: x.astype(str) if x.dtype == 'float' else x)
        if int(size) != 0:
            return {
                "file":file,
                "total": len(data),
                "header": data.columns.to_list(),
                "data": data.head(int(size)).to_dict(orient='records')
            }
        size = len(data)
        return {
            "file":file,
            "total": len(data),
            "header": data.columns.to_list(),
            "data": data.head(int(size)).to_dict(orient='records')
        }
    return None


def load_datasetHeader(filename, size=0):

    file_path = file_server_path_file+filename
    type_file = get_file_extension(filename).replace('.', "").strip()
    data = None

    try:

        with open(file_path, 'rb') as raw_data:
            result = chardet.detect(raw_data.read(1000))
        encoding = result['encoding']

        if type_file == 'csv':
            try:
                data = pd.read_csv(file_path, encoding=encoding,
                                   on_bad_lines="skip")
            except UnicodeDecodeError:
                data = pd.read_csv(file_path, encoding="latin1",
                                   on_bad_lines="skip")

        elif type_file == 'json':

            try:
                data = pd.read_json(file_path, encoding=encoding)

            except Exception as e:

                print(e)
        elif type_file == 'txt':

            data = pd.read_csv(file_path, encoding=encoding,
                               delimiter=detect_delimiter(file_path))
        elif type_file == 'xlsx':

            data = pd.read_excel(file_path)

    except FileNotFoundError as e:

        print(e)
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    group_numeric = data.select_dtypes(include=numerics)
    msg = []
    for col in group_numeric.columns.to_list():
        respone ={
            "value":col,
            "label":col
        }
        msg.append(respone)
    if data is not None and not data.empty:

        data = data.where(pd.notnull(data), None)
        data = data.apply(lambda x: x.astype(str) if x.dtype == 'float' else x)

        if int(size) != 0:
            return {
                "header": data.columns.to_list(),
                "header_label":msg,
                "header_numeric":group_numeric.columns.to_list(),
            }

        return {
            "header": data.columns.to_list(),
            "header_label":msg,
            "header_numeric":group_numeric.columns.to_list(),
        }
    return None


def remove_file(filename):
    path_file = file_server_path_file+filename
    if file_utile.find_file_by_filename(filename):
        os.remove(path_file)
        return True
    return False

def download_file(filename):

    file_path=file_server_path_file+filename
    if file_utile.find_file_by_filename(filename):

        if os.path.exists(file_path):
        
            with open(file_path, 'rb') as file:
        
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
    
    return None
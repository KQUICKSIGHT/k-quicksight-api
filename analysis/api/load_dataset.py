import random
import csv
import chardet
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
import uuid

from scipy.stats import f_oneway
import statsmodels.api as sm
from statsmodels.formula.api import ols

from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np


import matplotlib
matplotlib.use('Agg')


dotenv_path_dev = '.env'
load_dotenv(dotenv_path=dotenv_path_dev)

file_server_path_file = os.getenv("FILE_SERVER_PATH_FILE")
file_server_path_image = os.getenv("FILE_SERVER_PATH_IMAGE")
file_base_url = os.getenv("BASE_URL_FILE")

ALLOWED_EXTENSIONS_FILE = ['.csv', '.json', '.txt', '.xlsx']



def get_file_extension(filename):
    _, extension = os.path.splitext(filename)
    return extension


def detect_delimiter(file_path):
    with open(file_path, 'r') as file:
        sample = file.read(1024) 
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter




def load_dataset(filename):

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
        return data

    return None
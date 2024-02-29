import random
import csv
import chardet
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
import uuid
import seaborn as sns
from sklearn.impute import SimpleImputer

from scipy.stats import f_oneway
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import re
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import json
from itertools import combinations

import openai

import matplotlib
matplotlib.use('Agg')
color_graph ="#0346A5"


dotenv_path_dev = '.env'
load_dotenv(dotenv_path=dotenv_path_dev)

file_server_path_file = os.getenv("FILE_SERVER_PATH_FILE")
file_server_path_image = os.getenv("FILE_SERVER_PATH_IMAGE")
file_base_url = os.getenv("BASE_URL_FILE")

ALLOWED_EXTENSIONS_FILE = ['.csv', '.json', '.txt', '.xlsx']






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
        for col in data.columns:
            data.rename(columns={col: str(col).strip()}, inplace=True)

        numeric_columns = view_type_load_dataset(data)["numeric_columns"]
        for col in numeric_columns:
            data[col]= pd.to_numeric(data[col].replace('[^0-9.]', '', regex=True), errors='coerce')
        return data

    return None

def view_type_load_dataset(data):

    if data is not None:
        numeric_columns = []
        object_columns = []

        for column in data.columns:
            original_type = str(data[column].dtype)

            if original_type == 'object':

                numeric_values = data[column].astype(str).str.extract(r'(\d+)', expand=False)
                if not numeric_values.dropna().empty:

                    if find_character(str(data[column].head(1).iloc[0])):
                        object_columns.append(column)
                    else:    
                        numeric_columns.append(column)
                else:
                    object_columns.append(column)
            else:
                numeric_columns.append(column)

        return {
            "count_header": len(data.columns),
            "count_records": len(data),
            "all_columns": data.columns.tolist(),
            "numeric_columns": numeric_columns,
            "object_columns": object_columns
        }
    
    return None




def find_character(text):

    regex_pattern = r'[A-Za-z]'
    matches = re.findall(regex_pattern, text)

    if matches: 
        return True
    return False


def descrptive_statisitc(filename):

    data = load_dataset(filename)
    descriptive_stats = data.describe()
    return descriptive_stats.to_dict(orient="index")


def perform_analysis(filename,model_name="simple_linear_regression", 
                     independent_variable=None,alpha=None,list_range_numeric=[],
                     dependent_variable=None,
                     predict_values=200,
                     hypothesis_mean_column=None,
                     sample_mean=None,
                     list_paired_samples=None,
                     number_of_day_to_forecast=None,
                     column_date=None,
                     number_column=None,
                     degree=2):

    respone = {}
    if model_name == "simple_linear_regression":
        return simple_linear_regression(filename,independent_variable,dependent_variable,predict_values=predict_values)

    elif model_name == "non_linear_regression":
        return non_linear_regression(filename=filename,independent_variable=independent_variable,dependent_variable=dependent_variable,degree=degree,predict_values=predict_values,)

    elif model_name == "multiple_linear_regression":
        return multiple_linear_regression(filename=filename,independent_variables=independent_variable,dependent_variable=dependent_variable)
   
    elif model_name == "covariance":
        return find_covariance(filename,independent_variable,dependent_variable)

    elif model_name == "descriptive_statistic":
        return descrptive_statisitc(filename=filename)

    elif model_name == "random_number_generation":
        return random_number(filename=filename)

    elif model_name == "correlation":
        return find_correlation(filename,independent_variable,dependent_variable)
    
    elif model_name == "one_way_anova":
        return find_anova_single_factor(filename,list_range_numeric)
    
    elif model_name == "two_way_anova":
        return perform_two_way_anova(filename=filename,independent_variables=independent_variable,dependent_variable=dependent_variable)
    
    elif model_name == "one_sample_t_test":
        return find_one_sample_t_test(filename,sample_mean_name=hypothesis_mean_column,hypothesis_mean=sample_mean)

    elif model_name == "two_sample_t_test":
        return find_two_sample_t_tests(filename,independent_variable)

    elif model_name == "paired_t_test":
        return find_paired_t_test(filename,list_paired_samples)

    elif model_name == "exponential_smoothing":
        return find_exponential_smoothing(filename,number_of_day_to_forecast,column_date,number_column)
    
    
def find_exponential_smoothing(filename,number_of_day_to_forecast,column_date,number_column):
    try:
        # Load the dataset
        data = load_dataset(filename)

        # Convert the date column to datetime format and set the frequency to daily
        data['Date'] = pd.to_datetime(data['Date'])
        data = data.set_index('Date')
        data.index = pd.DatetimeIndex(data.index).to_period('D')

        # Create the series using the 'Value' column
        series = data['Value']

        # Apply simple exponential smoothing
        ses = SimpleExpSmoothing(series)
        model = ses.fit(smoothing_level=0.5, optimized=False)

        # Forecast
        forecast = model.forecast(number_of_day_to_forecast)
        data_dict = {forecast.strftime('%Y-%m-%d'): value for forecast, value in forecast.items()}

        return {
            "forecast": data_dict,
            "column_date":column_date,
            "number_column":number_column,
        }
    
    except Exception as e:
        return f"Error message: {e}"

def find_one_sample_t_test(filename,sample_mean_name,hypothesis_mean):
    try:
        data = load_dataset(filename)
        
        hypothesis_mean = float(hypothesis_mean)

        t_stat, p_value = stats.ttest_1samp(data[sample_mean_name], hypothesis_mean)

        return {
            "t-statistic": t_stat,
            "p_value": p_value,
            "column_name":sample_mean_name
        }
    
    except Exception as e:
        print(e)
    return None




def find_two_sample_t_tests(filename, independent_variables):
    try:
        data = load_dataset(filename)

        results = {}
        # Iterate over all combinations of two variables
        for group1_name, group2_name in combinations(independent_variables, 2):
            group1 = data[group1_name]
            group2 = data[group2_name]

            # Perform the two-sample t-test
            t_stat, p_value = stats.ttest_ind(group1, group2)

            # Store the results
            key = f"{group1_name} vs {group2_name}"
            results[key] = {
                "t-statistic": t_stat,
                "p_value": p_value,
                "column_name":independent_variables
            }

        return results
    except Exception as e:
        print(e)
        return None

def find_paired_t_test(filename,independent_variables):
    try:
        data = load_dataset(filename)

        results = {}
        # Iterate over all combinations of two variables
        for group1_name, group2_name in combinations(independent_variables, 2):
            group1 = data[group1_name]
            group2 = data[group2_name]

            # Perform the two-sample t-test
            t_stat, p_value = stats.ttest_rel(group1, group2)

            # Store the results
            key = f"{group1_name} vs {group2_name}"
            results[key] = {
                "t-statistic": t_stat,
                "p_value": p_value,
                "column_name":independent_variables
            }

        return results
    except Exception as e:
        print(e)
        return None
# recommendation 
def recommendation(filename,model_name,results):

    try:
        data = load_dataset(filename).head(10)
        recommend = perform_recommendation(str(data),model_name,str(results))
        return recommend
    except Exception as e:
        print(e)
    return None

openai.api_key = "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"

def perform_recommendation(data_values_str, model_name, results):
    prompt = """I want 2-3 lines of recommendation for analysis to non-technical users (Make it simple and easy to understand) based on the following information:

    First 10 rows of the dataset:
    %s

    Analysis model used: %s
    Analysis Result:
    %s

    Please provide a concise recommendation without headings, greetings, or descriptions. Just give me 2-3 lines of recommendation that can be used for analysis and decision-making.
    """ % (data_values_str, model_name, results)

    try:
        messages = [{"role": "system", "content": "You are a helpful assistant that provides information."},
                    {"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    
    except openai.error.AuthenticationError:
        print("Error: The API key is invalid or has expired. Please update your OpenAI API key and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def create_anova_formula(dependent_variable, independent_variables):
    main_effects = [f'C({var})' for var in independent_variables]
    two_way_interactions = [f'C({var1}):C({var2})' for i, var1 in enumerate(independent_variables) for var2 in independent_variables[i+1:]]
    three_way_interactions = [f'C({v1}):C({v2}):C({v3})' for i, v1 in enumerate(independent_variables) for j, v2 in enumerate(independent_variables[i+1:]) for v3 in independent_variables[j+1:]]

    formula_parts = main_effects + two_way_interactions + three_way_interactions
    formula = f'{dependent_variable} ~ {" + ".join(formula_parts)}'
    return formula

def replace_nan_with_none(value):
    if pd.isna(value):
        return None
    return value

def perform_two_way_anova(filename, dependent_variable, independent_variables):
    try:

        data = load_dataset(filename)
        formula = create_anova_formula(dependent_variable,independent_variables)
        model = ols(formula, data=data).fit()
        anova_results = anova_lm(model)
        anova_results = anova_results.fillna(0).to_dict(orient="index")

        return {
            "anova_result":anova_results,
            "variable_one":dependent_variable,
            "variable_two":dependent_variable
        }
    except Exception as e:
        print (e)

    return None



def find_anova_single_factor(filename, list_range_numeric):
    try:
        data = load_dataset(filename)

        # Convert data columns to numeric
        for col in list_range_numeric:
            data[col] = pd.to_numeric(data[col], errors='coerce')

        # Preparing the summary table
        sums = {col: data[col].sum().item() for col in list_range_numeric}
        averages = {col: data[col].mean().item() for col in list_range_numeric}
        counts = {col: int(data[col].count()) for col in list_range_numeric}
        variances = {col: data[col].var().item() for col in list_range_numeric}

        # Perform ANOVA
        st, pv = stats.f_oneway(*[data[col] for col in list_range_numeric])

        summary_table = {
            "sum": sums,
            "average": averages,
            "count": counts,
            "variance": variances,
            "anova": {
                "statistic": st.item(),
                "pvalue": pv.item(),
            },
            "column_name": list_range_numeric,
        }

        return {
            "groups": list_range_numeric,
            "summary_table": summary_table
        }

    except Exception as e:
        print(e)
    return None

def get_file_extension(filename):

    _, extension = os.path.splitext(filename)
    return extension


def detect_delimiter(file_path):
    with open(file_path, 'r') as file:
        sample = file.read(1024)  # Read a sample of the file
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter


def random_number(filename):
    data_random = {}
    data = descrptive_statisitc(filename)

    for column in data["max"]:
        max_val = data["max"][column]
        min_val = data["min"][column]

        random_values = [random.randint(min_val, max_val) for _ in range(20)]

        data_random[column] = random_values

    return data_random


def find_correlation(filename, variable_1, variable_2):
    try:
        # Load the dataset
        data = load_dataset(filename)

        # Check if both variables are in the dataset
        if variable_1 not in data.columns or variable_2 not in data.columns:
            return {"error": f"One or both variables not found in the dataset: {variable_1}, {variable_2}"}

        # Calculate and return the correlation
        correlation = data[[variable_1, variable_2]].corr().to_dict(orient="index")
        plt.scatter(data[variable_1], data[variable_2])
        plt.xlabel(variable_1)
        plt.ylabel(variable_2)
        plt.title(f'Scatter Plot of {variable_1} vs {variable_2}')
        filename_visualize = uuid.uuid4().hex + ".png"
        plt.savefig(file_server_path_image+filename_visualize)
        correlation["visulaize"]=filename_visualize
        correlation["variable_one"]=variable_1
        correlation["variable_two"]=variable_2
        return correlation

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def find_covariance(filename, variable_1, variable_2):
    try:
        # Load the dataset
        data = load_dataset(filename)
        
        if variable_1 in data.columns and variable_2 in data.columns:

            covariance = data[[variable_1, variable_2]].cov()
            plt.scatter(data[variable_1], data[variable_2])
            plt.xlabel(variable_1)
            plt.ylabel(variable_2)
            plt.title(f'Scatter Plot of {variable_1} vs {variable_2}')
            filename_visualize = uuid.uuid4().hex + ".png"
            plt.savefig(file_server_path_image+filename_visualize)
            covariance=covariance.to_dict(orient="index")
            covariance["visulaize"]=filename_visualize
            covariance["variable_one"]=variable_1
            covariance["variable_two"]=variable_2
            return covariance
        
        else:
            print(
                f"One or both variables not found in the dataset: {variable_1}, {variable_2}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")



def generate_anova_formula(dataframe, response_var):

    factor_vars = dataframe.columns.drop(response_var)
    formula_terms = [f'C({var})' for var in factor_vars]
    formula = f'{response_var} ~ {" + ".join(formula_terms)}'
    return formula





def find_anova_factor_two_with_replication(filename, variable):

    try:

        data = load_dataset(filename)
        str_type = ['str', 'object']
        group_numeric = data.select_dtypes(include=str_type)
        model = ols()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return None


def simple_linear_regression(filename, independent_variable, dependent_variable, predict_values=100):
    try:
        # Load dataset
        data = load_dataset(filename)

        X = data[[independent_variable]].values
        y = data[dependent_variable].values

        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # Training the model
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        predicted_value = model.predict([[predict_values]])

        X = sm.add_constant(X)
        model_stats = sm.OLS(y, X).fit()

        regression_statistics = {
            "multiple_r": (model_stats.rsquared)*2,
            "r_squared": model_stats.rsquared,
            "adjected_r_squared": model_stats.rsquared_adj,
            "f_statistic": model_stats.fvalue,
            "p_value": model_stats.f_pvalue,
            "observations": len(data),
            "stardard_error": model_stats.bse[1]
        }

        conefficient_summary_table = {
            "header": model_stats.summary().tables[1].data[0],
            "const": [element.strip() for element in model_stats.summary().tables[1].data[1]],
            "X": [element.strip() for element in model_stats.summary().tables[1].data[2]]
        }

        plt.figure(figsize=(15, 8))  
        plt.scatter(X_test, y_test, label="Testing Data",color=color_graph)
        plt.plot(X_test, y_pred, label="Linear Regression Prediction", color='r')
        plt.xlabel(independent_variable)
        plt.ylabel(dependent_variable)
        plt.title(f'Regression for {dependent_variable} vs {independent_variable}')
        filename_visualize = uuid.uuid4().hex + ".png"
        plt.savefig(file_server_path_image+filename_visualize)       

        return {
            "predict_value": predicted_value[0],
            "coefficient": model.coef_[0],
            "evaluate_model":evaluate_model(y_pred,y_test),
            "intercept": model.intercept_,
            "kurtosis": str(model_stats.summary().tables[2].data[2][1]).strip(),
            "skew": str(model_stats.summary().tables[2].data[3][1]).strip(),
            "regression_statistics": regression_statistics,
            "conefficient_summary_table": conefficient_summary_table,
            "visulaize":filename_visualize,
            "independent_variable":independent_variable,
            "dependent_variable":dependent_variable
        }

    except Exception as e:
        print(f"An error occurred simple linear: {str(e)}")

    return None


def non_linear_regression(filename, independent_variable, dependent_variable, degree=2, predict_values=100):

    try:
        # Load dataset
        data = load_dataset(filename)

        # Extracting independent and dependent variables
        X = data[[independent_variable]].values
        y = data[dependent_variable].values

        # Polynomial feature transformation
        polynomial_features = PolynomialFeatures(degree=degree)
        X_poly = polynomial_features.fit_transform(X)

        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X_poly, y, test_size=0.2, random_state=42)

        # Training the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predicting on test data
        y_pred = model.predict(X_test)

        # Predicting on custom values
        custom_value_poly = polynomial_features.fit_transform(
            [[predict_values]])
        predicted_value = model.predict(custom_value_poly)

        # Calculate statistics using statsmodels
        X_sm = sm.add_constant(X_poly)
        model_stats = sm.OLS(y, X_sm).fit()

        evaluate_model_stats = evaluate_model(y_pred=y_pred, y_test=y_test)
        regression_stat = regression_statistics(model_stats, len(data))
        coffi_sum_table = coefficient_summary_table(model_stats)
        descriptive_stats = summary_stat(data)
        
        
        plt.scatter(X_train, y_train, label="Training Data")
        plt.scatter(X_test, y_test, label="Testing Data")
        plt.plot(X_test, y_pred, label="Linear Regression Prediction", color='r')
        plt.xlabel(independent_variable)
        plt.ylabel(dependent_variable)
        plt.title(f'Scatter Plot and Linear Regression for {dependent_variable} vs {independent_variable}')
        filename_visualize = uuid.uuid4().hex + ".png"
        plt.savefig(file_server_path_image+filename_visualize)    


        return {
            "predict_value": predicted_value[0],
            "coefficient": model.coef_[0],
            "intercept": model.intercept_,
            "kurtosis": str(model_stats.summary().tables[2].data[2][1]).strip(),
            "skew": str(model_stats.summary().tables[2].data[3][1]).strip(),
            "evaluate_model": evaluate_model_stats,
            "descriptive_statstics": descriptive_stats,
            "regression_statistics": regression_stat,
            "conefficient_summary_table": coffi_sum_table,
            "visulaize":filename_visualize,
            "independent_variable":independent_variable,
            "dependent_variable":dependent_variable

        }

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return None


def multiple_linear_regression(filename, independent_variables, dependent_variable):

    try:



        data = load_dataset(filename)  
        data.fillna(0, inplace=True)

        X = data[independent_variables]
        y = data[dependent_variable]


        nan_rows = data[data.isna().any(axis=1)]

        print(nan_rows)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        # Training the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        X = sm.add_constant(X)

        model_stats = sm.OLS(y, X).fit()
        
        evaluate_model_stats = evaluate_model(y_pred=y_pred, y_test=y_test)
        regression_stat = regression_statistics(model_stats, len(data))

        descriptive_stats = summary_stat(data)
        X_train = np.array(X_train)
        X_test = np.array(X_test)

        visualizes =[]

        for i in range(X_train.shape[1]):
             
            plt.figure(figsize=(15, 8))  
            plt.scatter(X[independent_variables[i]], y, label="Data Points")
            # plt.plot(X[independent_variables[i]], model.predict(X[independent_variables]), color='red', linewidth=2, label="Regression Line")
        
            # Create a grid for the ith feature
            feature_grid = np.linspace(X[independent_variables[i]].min(), X[independent_variables[i]].max(), 100)
            
            # Create an array where all features are set to their mean values
            X_pred = np.full((len(feature_grid), X_train.shape[1]), X_train.mean(axis=0))
            
            # Replace the ith feature in X_pred with the values from feature_grid
            X_pred[:, i] = feature_grid

            # Predict using the model
            predicted = model.predict(X_pred)

            # Plot the regression line
            plt.plot(feature_grid, predicted, color='red', linewidth=2, label="Regression Line")


            plt.xlabel(independent_variables[i])
            plt.ylabel(dependent_variable)
            plt.title(f'Scatter Plot for {dependent_variable} vs {independent_variables[i]}')

            filename_visualize = uuid.uuid4().hex + ".png"
            plt.legend()
            plt.savefig(file_server_path_image + filename_visualize)
            visualizes.append(filename_visualize)

        return {
            "kurtosis": str(model_stats.summary().tables[2].data[2][1]).strip(),
            "skew": str(model_stats.summary().tables[2].data[3][1]).strip(),
            "evaluate_model":evaluate_model_stats,
            "coefficient": dict(zip(independent_variables, model.coef_)),
            "intercept": model.intercept_,
            "descriptive_statistics":descriptive_stats,
            "regression_statistics": regression_stat,
            "visualizes":visualizes,
            "independent_variable":independent_variables,
            "dependent_variable":dependent_variable
        }

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return None


def evaluate_model(y_pred, y_test):

    return {
        "R2": r2_score(y_pred, y_test),
        "MAE": mean_absolute_error(y_pred, y_test),
        "MSE": mean_squared_error(y_pred, y_test),
        "RMSE": np.sqrt(mean_absolute_error(y_pred, y_test))
    }


def regression_statistics(model_stats, length):

    return {
        "multiple_r": model_stats.rsquared,
        "adjusted_r_squared": model_stats.rsquared_adj,
        "f_statistic": model_stats.fvalue,
        "p_value": model_stats.f_pvalue,
        "observations": length,
        "standard_error": model_stats.bse[1]
    }


def summary_stat(data):
    descriptive_stats = data.describe()
    return descriptive_stats.to_dict(orient="index")


def coefficient_summary_table(model_stats):

    return {
        "header": model_stats.summary().tables[1].data[0],
        "const": [element.strip() for element in model_stats.summary().tables[1].data[1]],
        "variables": [element.strip() for element in model_stats.summary().tables[1].data[2]]
    }

# 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
def exploratory_data_analysis(filename, visualizes,indepeden_vairable,dependent_variable):

    try:

        data = load_dataset(filename)
        numeric_columns = [indepeden_vairable,dependent_variable]

        correlation = data[numeric_columns].corr().to_dict(orient="index")
        descriptive_stats = data.describe().to_dict(orient="index")
        visualization = visualize_graph(visualizes, data, indepeden_vairable,dependent_variable)

        message = {
            "headers": data.columns,
            "number_headers": numeric_columns,
            "correlation": correlation,
            "descriptive_stats": descriptive_stats,
            "visualization": visualization,
        }
        return message

    except Exception as e:
        print(f"An error occurred eda: {str(e)}")

    return None


def visualize_graph(list_of_visualization, data, independent_variable, dependent_variable):

    response = {}  
    for visualization in list_of_visualization:
        if visualization == 'scatter_plot':
            scatter = scatter_plot_two_variables(data, independent_variable, dependent_variable)
            response['scatter'] = scatter

        elif visualization == 'histogram':
            histogram = histogram_two_variables(data, independent_variable, dependent_variable)
            response['histogram'] = histogram

        elif visualization == 'boxplot':
            boxplot = boxplot_two_variables(data, independent_variable, dependent_variable)
            response['boxplot'] = boxplot
        
        elif visualization == 'line_chart':
            line_chart = line_chart_two_variables(data, independent_variable, dependent_variable)
            response["line_chart"] = line_chart 

    return response



def boxplot_two_variables(data, x_variable, y_variable):

    plt.figure(figsize=(8, 6)) 
    plt.boxplot(data[y_variable], vert=False)
    plt.title(f'Boxplot of {y_variable} by {x_variable}')
    plt.xlabel(y_variable)
    plt.ylabel(x_variable)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    filename_visualize = uuid.uuid4().hex + ".png"
    plt.savefig(file_server_path_image + filename_visualize)

    return filename_visualize



def histogram_two_variables(data, x_variable, y_variable, bins=10):

    plt.figure(figsize=(8, 6))  
    plt.hist(data[x_variable],bins=bins)
    plt.title(f'Histogram of {y_variable} by {x_variable}')
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    filename_visualize = uuid.uuid4().hex + ".png"
    plt.savefig(file_server_path_image + filename_visualize)

    return filename_visualize


def line_chart_two_variables(data, x_variable, y_variable):

    plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
    plt.plot(data[x_variable], data[y_variable], marker='o', linestyle='-', color=color_graph)
    plt.title(f'Line Chart: {y_variable} by {x_variable}')
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.grid(True, linestyle='--', alpha=0.7)
    filename_visualize = uuid.uuid4().hex + ".png"
    plt.savefig(file_server_path_image + filename_visualize)

    return filename_visualize



def scatter_plot_two_variables(data, x_variable, y_variable):

    plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
    plt.scatter(data[x_variable], data[y_variable], marker='o', color=color_graph)
    plt.title(f'Scatter Plot: {y_variable} by {x_variable}')
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.grid(True, linestyle='--', alpha=0.7)
    filename_visualize = uuid.uuid4().hex + ".png"
    plt.savefig(file_server_path_image + filename_visualize)

    return filename_visualize


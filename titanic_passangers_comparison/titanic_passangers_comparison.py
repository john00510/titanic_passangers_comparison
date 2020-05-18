"""Docstring"""
import sys
import os
import json
import pickle
from argparse import ArgumentParser
import pandas as pd
from pandas import json_normalize
import requests
import numpy as np

from settings import json_base_dataset_path
from settings import csv_new_dataset_path
from settings import output_dirpath

def unique_values_func(**kwargs):
    """Docstring"""
    return {'column': kwargs['key'], '"{}" value'.format(kwargs['df1_name']): kwargs['val1'],\
        '"{}" value'.format(kwargs['df2_name']): kwargs['val2'], 'index': kwargs['name']}

def normalize_float(fl_num):
    """Docstring"""
    if isinstance(fl_num, float, np.float64):
        return round(fl_num, 10)
    return fl_num

def normalize_json_data(dframe):
    """Docstring"""
    dframe = json_normalize(dframe)
    dframe = dframe.drop([c for c in dframe.columns if '.' not in c], axis=1)
    dframe.columns = [c.split('.')[1].lower() for c in dframe.columns]
    dframe = dframe.reindex(sorted(dframe.columns), axis=1)
    return dframe

def normalize_csv_column_names(dframe):
    """Docstring"""
    dframe.columns = [c.lower() for c in dframe.columns]
    dframe = dframe.reindex(sorted(dframe.columns), axis=1)
    return dframe

def print_json(j):
    """Docstring"""
    print(json.dumps(j, indent=2))

def dataset_in_dataset(unique_values, unique_indices, df1, df2):
    """Docstring"""
    return len(unique_indices) == 0 and len(unique_values) == 0 and\
        len(df1) > 0 and len(df2) > 0

class TitanicPassangersComparison():
    """Docstring"""
    def __init__(self):
        self.datasets = {}
        self.report = {}
        self.df1 = None
        self.df2 = None
        self.df1_name = None
        self.df2_name = None

    def load_dataset(self, path_uri, name):
        """Docstring"""
        if path_uri.startswith('http'):
            resp = requests.get(path_uri)
            json_data = resp.json().get('records')
            data_frame = normalize_json_data(json_data)
            data_frame.set_index('name', drop=True, inplace=True)
            self.datasets[name] = data_frame

        elif path_uri.endswith('json'):
            with open(path_uri) as f_handler:
                json_data = json.load(f_handler)
                data_frame = normalize_json_data(json_data)
                data_frame.set_index('name', drop=True, inplace=True)
                self.datasets[name] = data_frame

        elif path_uri.endswith('csv'):
            data_frame = pd.read_csv(path_uri, delimiter=';')
            data_frame = normalize_csv_column_names(data_frame)
            data_frame.set_index('name', drop=True, inplace=True)
            self.datasets[name] = data_frame

        else:
            sys.exit('Dataset path error!')

    def compare_datasets(self, df1_name, df2_name, index=None):
        """Docstring"""
        self.df1_name = df1_name
        self.df2_name = df2_name

        self.df1 = self.datasets[self.df1_name]
        self.df2 = self.datasets[self.df2_name]
        if index:
            self.df1 = self.df1[self.df1.index == index]
            self.df2 = self.df2[self.df2.index == index]

        self.compare_columns(df1=self.df1, df2=self.df2, df1_name=self.df1_name,\
            df2_name=self.df2_name)

        self.report['datasets'][df1_name]['length'] = len(self.df1)
        self.report['datasets'][df2_name]['length'] = len(self.df2)

        if self.df1 and self.df2:
            self.compare_rows(df1=self.df1, df2=self.df2, df1_name=self.df1_name,\
                df2_name=self.df2_name)

            self.compare_rows(df1=self.df2, df2=self.df1, df1_name=self.df2_name,\
                df2_name=self.df1_name)

    def compare_columns(self, df1, df2, df1_name, df2_name):
        """Docstring"""
        df1_columns = list(df1.columns) + [df1.index.name]
        df2_columns = list(df2.columns) + [df2.index.name]

        self.report['columns in common'] = list(set(df1_columns)&set(df2_columns))
        self.report['unique columns'] = list(set(df1_columns)^set(df2_columns))
        self.report['columns total'] = self.report['columns in common'] +\
            self.report['unique columns']

        self.report['datasets'] = {}
        self.report['datasets'][df1_name] = {}
        self.report['datasets'][df1_name]['columns'] = df1_columns
        self.report['datasets'][df1_name]['unique values'] = []
        self.report['datasets'][df1_name]['unique indices'] = []

        self.report['datasets'][df2_name] = {}
        self.report['datasets'][df2_name]['columns'] = df2_columns
        self.report['datasets'][df2_name]['unique values'] = []
        self.report['datasets'][df2_name]['unique indices'] = []

    def compare_rows(self, df1, df2, df1_name, df2_name):
        """Docstring"""
        for name, data in df1.iterrows():
            _df2 = df2.loc[df2.index == name]
            #if  len(_smaller_df) > 1:
            #   self.duplicate_rows()

            if len(_df2) == 1:
                self.compare_values(data1=data, name1=name, data2=_df2.iloc[0],\
                    df1_name=df1_name, df2_name=df2_name)

            else:
                self.compare_indices(df_name=df1_name, index=name)

    def compare_values(self, **kwargs):
        """Docstring"""
        keys = kwargs['data1'].keys().tolist()
        values1 = kwargs['data1'].tolist()
        values2 = kwargs['data2'].tolist()

        unique_values = self.report['datasets'][kwargs['df1_name']]['unique values']
        for i, key in enumerate(keys):
            val1, val2 = values1[i], values2[i]

            val1 = normalize_float(val1)
            val2 = normalize_float(val2)

            if val1 != val2:
                if isinstance(val1, str) and isinstance(val2, str):
                    unique_value = unique_values_func(key=key, df1_name=kwargs['df1_name'],\
                        df2_name=kwargs['df2_name'], val1=val1, val2=val2, name=kwargs['name1'])

                    unique_values.append(unique_value)
                elif np.isnan(val1) is False and np.isnan(val2) is False:
                    unique_value = unique_values_func(key=key, df1_name=kwargs['df1_name'],\
                        df2_name=kwargs['df2_name'], val1=val1, val2=val2, name=kwargs['name1'])

                    unique_values.append(unique_value)

    def compare_indices(self, df_name, index):
        """Docstring"""
        unique_indices = self.report['datasets'][df_name]['unique indices']
        unique_indices.append(index)

    def print_datasets(self):
        """Docstring"""
        print('#'*150)
        print(self.df1_name, '\n')
        print(self.df1.head(), '\n')
        print('#'*150)
        print(self.df2_name, '\n')
        print(self.df2.head(), '\n')

    def print_report(self):
        """Docstring"""
        datasets = self.report['datasets']
        datasets_names = list(datasets.keys())

        print('"{}" and "{}" have {} common columns'.format(datasets_names[0],\
            datasets_names[1], len(self.report['columns in common'])))

        print('"{}" and "{}" have {} unique columns\n'.format(datasets_names[0],\
            datasets_names[1], len(self.report['unique columns'])))

        for key in datasets:
            key2 = [x for x in datasets_names if x != key][0]
            columns = datasets[key]['columns']
            unique_indices = datasets[key]['unique indices']
            unique_values = datasets[key]['unique values']

            print('"{}" has {} columns'.format(key, len(columns)))
            print('"{}" has {} unique {}'.format(key, len(unique_indices),\
                'index' if len(unique_indices) == 1 else 'indices'))

            print('"{}" has {} unique {}'.format(key, len(unique_values),\
                'value' if len(unique_values) == 1 else 'values'))

            print('"{}" in "{}": {}\n'.format(key, key2, dataset_in_dataset(\
                unique_values=unique_values, unique_indices=unique_indices,\
                df1=self.df1, df2=self.df2)))

        #self.print_json(self.report)

    def save_report(self):
        """Docstring"""
        path = os.path.join(output_dirpath, '{} {}.pkl'.format(self.df1_name, self.df2_name))
        with open(path, 'wb') as f_handler:
            pickle.dump(self.report, f_handler)

if __name__ == '__main__':
    PARSER = ArgumentParser()

    PARSER.add_argument('-dataset1_path', default=json_base_dataset_path,\
        help='Path of the base dataset')
    PARSER.add_argument('-dataset1_name', default='Base dataset',\
        help='Name of the base dataset')

    PARSER.add_argument('-dataset2_path', default=csv_new_dataset_path,\
        help='Path of the dataset for comparison')
    PARSER.add_argument('-dataset2_name', default='New dataset',\
        help='Name of the dataset for comparison')

    PARSER.add_argument('-index', help='Comparison of the datasets by index')

    ARGS = vars(PARSER.parse_args())

    CLS = TitanicPassangersComparison()
    CLS.load_dataset(path_uri=ARGS['dataset1_path'], name=ARGS['dataset1_name'])
    CLS.load_dataset(path_uri=ARGS['dataset2_path'], name=ARGS['dataset2_name'])
    CLS.compare_datasets(df1_name=ARGS['dataset1_name'], df2_name=ARGS['dataset2_name'],\
        index=ARGS['index'])
    CLS.print_datasets()
    CLS.print_report()
    CLS.save_report()

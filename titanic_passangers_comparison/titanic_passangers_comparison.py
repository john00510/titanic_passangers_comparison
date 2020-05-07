from argparse import ArgumentParser
import pandas as pd
from pandas import json_normalize
import requests
import json
import numpy as np
import sys
import pickle
import os

from settings import csv_base_dataset_path
from settings import json_base_dataset_path
from settings import json_new_dataset_path
from settings import csv_new_dataset_path
from settings import json_dataset_uri
from settings import output_dirpath

class TitanicPassangersComparison(object):
	def __init__(self):
		self.datasets = {}
		self.report = {}
		
	def load_dataset(self, path_uri, name):
		if path_uri.startswith('http'):
			resp = requests.get(path_uri)
			json_data = resp.json().get('records')
			df = self.normalize_json_data(json_data)
			df.set_index('name', drop=True, inplace=True)
			self.datasets[name] = df

		elif path_uri.endswith('json'):
			with open(path_uri) as fh:
				json_data = json.load(fh)
				df = self.normalize_json_data(json_data)
				df.set_index('name', drop=True, inplace=True)				
				self.datasets[name] = df

		elif path_uri.endswith('csv'):
			df = pd.read_csv(path_uri, delimiter=';')
			df = self.normalize_csv_column_names(df)
			df.set_index('name', drop=True, inplace=True)
			self.datasets[name] = df

		else:
			sys.exit('Dataset path error!')

	def compare_datasets(self, df1_name, df2_name, index=None):
		self.df1_name = df1_name
		self.df2_name = df2_name

		self.df1 = self.datasets[self.df1_name]
		self.df2 = self.datasets[self.df2_name]
		if index:
			self.df1 = self.df1[self.df1.index == index]
			self.df2 = self.df2[self.df2.index == index]

		self.compare_columns(df1=self.df1, df2=self.df2, df1_name=self.df1_name, df2_name=self.df2_name)

		self.report['datasets'][df1_name]['length'] = len(self.df1)
		self.report['datasets'][df2_name]['length'] = len(self.df2)

		if len(self.df1) > 0 and len(self.df2) > 0:
			self.compare_rows(df1=self.df1, df2=self.df2, df1_name=self.df1_name, df2_name=self.df2_name)
			self.compare_rows(df1=self.df2, df2=self.df1, df1_name=self.df2_name, df2_name=self.df1_name)

	def compare_columns(self, df1, df2, df1_name, df2_name):
		df1_columns = list(df1.columns) + [df1.index.name]
		df2_columns = list(df2.columns) + [df2.index.name]

		self.report['columns in common'] = list(set(df1_columns)&set(df2_columns))
		self.report['unique columns'] = list(set(df1_columns)^set(df2_columns))
		self.report['columns total'] = self.report['columns in common'] + self.report['unique columns']

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
		for name, data in df1.iterrows():
			_df2 = df2.loc[df2.index == name]
			#if  len(_smaller_df) > 1:
			#	self.duplicate_rows()

			if len(_df2) == 1:
				self.compare_values(data1=data, name1=name, data2=_df2.iloc[0], 
					df1_name=df1_name, df2_name=df2_name)

			else:
				self.compare_indices(df_name=df1_name, index=name)

	def compare_values(self, data1, name1, data2, df1_name, df2_name):
		keys = data1.keys().tolist()
		values1 = data1.tolist()
		values2 = data2.tolist()

		unique_values = self.report['datasets'][df1_name]['unique values']
		for i in range(len(keys)):
			key, v1, v2 = keys[i], values1[i], values2[i]

			v1 = self.normalize_float(v1)
			v2 = self.normalize_float(v2)

			if v1 != v2:
				if type(v1) == str and type(v2) == str:
					unique_value = self.unique_values(key=key, df1_name=df1_name, df2_name=df2_name, v1=v1, v2=v2, name=name1)
					unique_values.append(unique_value)
				elif np.isnan(v1) == False and np.isnan(v2) == False:
					unique_value = self.unique_values(key=key, df1_name=df1_name, df2_name=df2_name, v1=v1, v2=v2, name=name1)
					unique_values.append(unique_value)

	def unique_values(self, key, df1_name, df2_name, v1, v2, name):
		return {'column': key, '"{}" value'.format(df1_name): v1, '"{}" value'.format(df2_name): v2, 'index': name}

	def compare_indices(self, df_name, index):
		unique_indices = self.report['datasets'][df_name]['unique indices']
		unique_indices.append(index)

	def normalize_float(self, f):
		if type(f) in [float, np.float64]:
			return round(f, 10)
		else:
			return f		

	def normalize_json_data(self, df):
		df = json_normalize(df)
		df = df.drop([c for c in df.columns if '.' not in c], axis=1)
		df.columns = [c.split('.')[1].lower() for c in df.columns]
		df = df.reindex(sorted(df.columns), axis=1)
		return df

	def normalize_csv_column_names(self, df):
		df.columns = [c.lower() for c in df.columns]
		df = df.reindex(sorted(df.columns), axis=1)
		return df

	def print_datasets(self):
		print('#'*150)
		print(self.df1_name, '\n')
		print(self.df1.head(), '\n')
		print('#'*150)
		print(self.df2_name, '\n')
		print(self.df2.head(), '\n')

	def print_report(self):
		datasets = self.report['datasets']
		datasets_names = list(datasets.keys())

		print('"{}" and "{}" have {} common columns'.format(datasets_names[0], datasets_names[1], len(self.report['columns in common'])))
		print('"{}" and "{}" have {} unique columns\n'.format(datasets_names[0], datasets_names[1], len(self.report['unique columns'])))

		for key in datasets:
			key2 = [x for x in datasets_names if x!=key][0]
			columns = datasets[key]['columns']
			unique_indices = datasets[key]['unique indices']
			unique_values = datasets[key]['unique values']

			print('"{}" has {} columns'.format(key, len(columns)))
			print('"{}" has {} unique {}'.format(key, len(unique_indices), 'index' if len(unique_indices) == 1 else 'indices'))
			print('"{}" has {} unique {}'.format(key, len(unique_values), 'value' if len(unique_values) == 1 else 'values'))
			print('"{}" in "{}": {}\n'.format(key, key2, self.dataset_in_dataset(unique_values=unique_values, unique_indices=unique_indices, 
				df1=self.df1, df2=self.df2)))

		#self.print_json(self.report)

	def save_report(self):
		path = os.path.join(output_dirpath, '{} {}.pkl'.format(self.df1_name, self.df2_name))
		with open(path, 'wb') as fh:
			pickle.dump(self.report, fh)

	def print_json(self, j):
		print(json.dumps(j, indent=2))

	def dataset_in_dataset(self, unique_values, unique_indices, df1, df2):
		return len(unique_indices) == 0 and len(unique_values) == 0 and len(df1) > 0 and len(df2) > 0

if __name__ == '__main__':
	parser = ArgumentParser()

	parser.add_argument('-dataset1_path', default=json_base_dataset_path, 
		help='Path of the base dataset')
	parser.add_argument('-dataset1_name', default='Base dataset', 
		help='Name of the base dataset')

	parser.add_argument('-dataset2_path', default=csv_new_dataset_path, 
		help='Path of the dataset for comparison')
	parser.add_argument('-dataset2_name', default='New dataset', 
		help='Name of the dataset for comparison')

	parser.add_argument('-index', help='Comparison of the datasets by index')

	args = vars(parser.parse_args())

	c = TitanicPassangersComparison()
	c.load_dataset(path_uri=args['dataset1_path'], name=args['dataset1_name'])
	c.load_dataset(path_uri=args['dataset2_path'], name=args['dataset2_name'])
	c.compare_datasets(df1_name=args['dataset1_name'], df2_name=args['dataset2_name'], index=args['index'])
	c.print_datasets()
	c.print_report()
	c.save_report()
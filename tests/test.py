import subprocess as sp
import sys

sys.path.append('../titanic_passangers_comparison')

from titanic_passangers_comparison import TitanicPassangersComparison

from settings import csv_base_dataset_path
from settings import json_base_dataset_path
from settings import json_new_dataset_path
from settings import csv_new_dataset_path
from settings import json_dataset_uri
from settings import output_dirpath

def test_base_to_new_datasets_comparison():
	c = TitanicPassangersComparison()
	c.load_dataset(path_uri=json_base_dataset_path, name='Base dataset')
	c.load_dataset(path_uri=csv_new_dataset_path, name='New dataset')
	c.compare_datasets(df1_name='Base dataset', df2_name='New dataset')
	report = c.report

	datasets = report['datasets']
	if datasets['Base dataset']['length'] > datasets['New dataset']['length']:
		print('Test_base_to_new_datasets_comparison succeed.')
	else:
		print('Test_base_to_new_datasets_comparison failed.')

def test_index_with_empty_dataframes():
	c = TitanicPassangersComparison()
	c.load_dataset(path_uri=json_base_dataset_path, name='Base dataset')
	c.load_dataset(path_uri=csv_new_dataset_path, name='New dataset')
	c.compare_datasets(df1_name='Base dataset', df2_name='New dataset', index='Collander, Mr. Erik Gusta')
	report = c.report

	datasets = report['datasets']
	if datasets['Base dataset']['length'] == 0 and datasets['New dataset']['length'] == 0:
		print('Test_index_with_empty_dataframes succeed.')
	else:
		print('Test_index_with_empty_dataframes failed.')

def test_index_with_one_record_match():
	c = TitanicPassangersComparison()
	c.load_dataset(path_uri=json_base_dataset_path, name='Base dataset')
	c.load_dataset(path_uri=csv_new_dataset_path, name='New dataset')
	c.compare_datasets(df1_name='Base dataset', df2_name='New dataset', index='Collander, Mr. Erik Gustaf')
	report = c.report

	datasets = report['datasets']
	if datasets['Base dataset']['length'] == 1 and datasets['New dataset']['length'] == 1:
		print('Test_index_with_one_record_match succeed.')
	else:
		print('Test_index_with_one_record_match failed.')

test_base_to_new_datasets_comparison()
test_index_with_empty_dataframes()
test_index_with_one_record_match()
import os

project_dirpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_base_dataset_path = os.path.join(project_dirpath, 'datasets/base_datasets/titanic-passengers.csv')
json_base_dataset_path = os.path.join(project_dirpath, 'datasets/base_datasets/titanic-passengers.json')

csv_new_dataset_path = os.path.join(project_dirpath, 'datasets/new_datasets/titanic-passengers.csv')
json_new_dataset_path = os.path.join(project_dirpath, 'datasets/new_datasets/titanic-passengers.json')

json_dataset_uri = 'https://public.opendatasoft.com/api/records/1.0/search/?dataset=titanic-passengers&facet=survived&facet=pclass&facet=sex&facet=age&facet=embarked&rows=1000'
output_dirpath = os.path.join(project_dirpath, 'output')
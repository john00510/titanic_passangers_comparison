1) DESCRIPTION
Titanic_passangers_comparison library compares 2 datasets against each other and provides a report in a console
and json report file. Datasets can be in JSON, CSV formats loaded locally or from REST API.

local path example: datasets/base_datasets/titanic-passengers.csv
REST API example: https://public.opendatasoft.com/api/records/1.0/search/?dataset=titanic-passengers

2) INSTALLATION
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps titanic_passangers_comparison-yuri0051

3) COMMAND EXAMPLES

python3 titanic_passangers_comparison.py
python titanic_passangers_comparison.py -dataset1_path https://public.opendatasoft.com/api/records/1.0/search/?dataset=titanic-passengers -dataset1_name 'Base dataset'\
  -dataset2_path datasets/base_datasets/titanic-passengers.csv -dataset2_name 'New dataset'

python3 titanic_passangers_comparison.py -index 'Collander, Mr. Erik Gusta'
python3 titanic_passangers_comparison.py -index 'Collander, Mr. Erik Gustaf'

Agruments: 

Path of the base dataset (has default value): -dataset1_path
Name of the base dataset (has default value): -dataset1_name
Path of the dataset for comparison (has default value): -dataset2_path
Name of the dataset for comparison (has default value): -dataset2_name
Comparison of the datasets by index (optional): -index

4) OUTPUT REPORT JSON FILE EXAMPLE
{
  "columns in common": [],
  "unique columns": [],
  "columns total": [],
  "datasets": {
    "Base dataset": {
      "columns": [],
      "unique values": [],
      "unique indices": [],
      "length": 1
    },
    "New dataset": {
      "columns": [],
      "unique values": [],
      "unique indices": [],
      "length": 1
    }
  }
}

5) PRINT MESSAGE IN A COLSOLE EXAMPLE

######################################################################################################################################################
Base dataset 

                             age cabin embarked  fare  parch  passengerid  pclass   sex  sibsp survived  ticket
name                                                                                                           
Collander, Mr. Erik Gustaf  28.0   NaN        S  13.0      0          343       2  male      0       No  248740 

######################################################################################################################################################
New dataset 

                             age cabin embarked  fare  parch  passengerid  pclass   sex  sibsp survived  ticket
name                                                                                                           
Collander, Mr. Erik Gustaf  28.0   NaN        S  13.0      0          343       2  male      0       No  248740 

"Base dataset" and "New dataset" have 12 common columns
"Base dataset" and "New dataset" have 0 unique columns

"Base dataset" has 12 columns
"Base dataset" has 0 unique indices
"Base dataset" has 0 unique values
"Base dataset" in "New dataset": True

"New dataset" has 12 columns
"New dataset" has 0 unique indices
"New dataset" has 0 unique values
"New dataset" in "Base dataset": True

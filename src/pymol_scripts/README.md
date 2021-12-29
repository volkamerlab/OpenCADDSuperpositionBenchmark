# pymol_scripts subfolder
This folder contains the scripts required to perform the alignments in PyMol and parse the output afterwards.

## pymol_between_groups_alignment.py

This script performs the pairwise alignments between structures of the two sample sets (groups) provided.

To call this file, a PyMol installation is required.

Before running the script, the paths to the sample sets need to be adjusted in the file.

The call is performed in the unix terminal:
```
pymol pymol_between_groups_alignment.py > <PATH_TO_OUTPUT_FILE>
```
The ```<PATH_TO_OUTPUT_FILE>``` needs to be adjusted in the call.

## pymol_in_group_alignment.py

This script performs the pairwise alignments between structures of one sample set (group) provided.

To call this file, a PyMol installation is required.

Before running the script, the paths to the sample sets need to be adjusted in the file.

The call is performed in the unix terminal:
```
pymol pymol_in_group_alignment.py > <PATH_TO_OUTPUT_FILE>
```
The ```<PATH_TO_OUTPUT_FILE>``` needs to be adjusted in the call.

## pymol_log_parser.py

This script is called in the unix terminal by:
```python3 pymol_log_parser.py```
while being in this folder.

Before calling the script the paths for the input file (log file of PyMol) and the output file (csv file representing the dataframe with the results) need to be adjusted.
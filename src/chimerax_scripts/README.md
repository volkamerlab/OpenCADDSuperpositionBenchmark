# chimerax_scripts subfolder
This folder contains the scripts required to perform the alignments in ChimeraX and parse the output afterwards.

## matchmaker_between_groups_alignment.py

This file is called in ChimeraX by opening the file in ChimeraX itself.
This script performs the pairwise alignments between structures of the two sample sets (groups) provided.
For that, the paths to the sample sets need to be adjusted in the file.
Additionally the output path of the log is required in the file.

## matchmaker_in_group_alignment.py

This file is called in ChimeraX by opening the file in ChimeraX itself.
This script performs the pairwise alignments between structures of one sample set (group) provided.
For that, the path to the sample set need to be adjusted in the file.
Additionally the output path of the log is required in the file.

## matchmaker_log_parser.py

This script is called in the unix terminal by:
```python3 matchmaker_log_parser.py```
while being in this folder.

Before calling the script the paths for the input file (log file of ChimeraX) and the output file (csv file representing the dataframe with the results) need to be adjusted.
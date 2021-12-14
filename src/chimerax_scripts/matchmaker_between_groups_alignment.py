"""
This script is called in ChimeraX to perform all alignments between two sample sets. 
In this project sample sets represent kinase groups, so the alignments are performed between structures of different groups.
Before calling this script in ChimeraX, the paths for the two sample sets have to be adjusted appropiately as well as the path where the logfile should be saved.
This logfile is parsed afterwards using the "matchmaker_log_parser.py" script, to convert the results into a *.csv file similar to the other methods.
"""
# open this script in ChimeraX

from chimerax.core.commands import run
import time

reference_strucs = []
with open("<PATH_TO_SAMPLE_SET1>") as f:
    # split line, so no newline characters are left
    # then split lines into lists to get the same structure as in the benchmark for OpenCADD
    temp = f.read().splitlines()
    for line in temp:
        struc = line.split(",")
        reference_strucs.append(struc)

mobile_strucs = []
with open("<PATH_TO_SAMPLE_SET2>") as f:
    # split line, so no newline characters are left
    # then split lines into lists to get the same structure as in the benchmark for OpenCADD
    temp = f.read().splitlines()
    for line in temp:
        struc = line.split(",")
        mobile_strucs.append(struc)

counter = 0

# iterate through all structures of the samples
for structure in reference_strucs:
    for mobile in mobile_strucs:
        # fetch pdb file with only the first model and get the length of structures (amount of CA)
        run(session, f"open {structure[0]} format pdb maxModels 1")
        print(f"reference: {structure} ")
        run(session, f"select #1/{structure[4]}@ca")
        run(session, f"open {mobile[0]} format pdb maxModels 1")
        print(f"mobile: {mobile} ")
        run(session, f"select #2/{mobile[4]}@ca")
        # run alignment on the selected chains and only CA without any cutoff score, so a global alignment is performed
        print(f"\nalignment: {counter} ")
        start_time = time.time()
        run(session, f"mmaker #1/{structure[4]}@ca to #2/{mobile[4]}@ca cut None")
        end_time = time.time()
        duration = round(end_time - start_time, 4)
        print(f"time: {duration} ")
        counter += 1
        # reset
        run(session, "close #1")
        run(session, "close #2")

# save logfile
run(session, 'log save "<PATH_WHERE_TO_STORE_THE_LOGFILE>"')

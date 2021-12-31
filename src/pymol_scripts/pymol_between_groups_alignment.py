"""
This script is used to run all alignments between two sample sets.
The paths to the sample set files need to be changed appropriately.
After changing the paths, run this script in the terminal by calling "pymol pymol_between_groups_alignment.py > <PATH_TO_OUTPUT_FILE>"
This output file is parsed afterwards using the "pymol_log_parser.py".
"""

from pymol import cmd
import time

# get all structures (the sample sets created before, so the same structures as for OpenCADD)
reference_strucs = []
with open("<PATH_TO_SAMPLE_SET1>") as f:
    # split line, so no newline characters are left
    # then split lines into lists to get the same structure as in the benchmark for the OpenCADD methods
    temp = f.read().splitlines()
    for line in temp:
        struc = line.split(",")
        reference_strucs.append(struc)

mobile_strucs = []
with open("<PATH_TO_SAMPLE_SET2>") as f:
    # split line, so no newline characters are left
    # then split lines into lists to get the same structure as in the benchmark for the OpenCADD methods
    temp = f.read().splitlines()
    for line in temp:
        struc = line.split(",")
        mobile_strucs.append(struc)

counter = 0

for structure in reference_strucs:
    for mobile in mobile_strucs:
        counter += 1
        print(counter)
        # set default to pdb download
        cmd.set("fetch_type_default", "pdb")
        cmd.fetch(structure[0])
        print(f"reference: {structure}")
        # get size of reference structure
        s1_size = cmd.select(f"n. CA and chain {structure[4]} and not alt A")
        print(f"reference_size: {s1_size}")
        # reinitialize to get the size of the other structure
        cmd.reinitialize()
        cmd.set("fetch_type_default", "pdb")
        cmd.fetch(mobile[0])
        print(f"mobile: {mobile}")
        # size of mobile structure
        mobile_size = cmd.select(f"n. CA and chain {mobile[4]} and not alt A")
        print(f"mobile_size: {mobile_size}")
        # have to fetch reference again, pymol saves all fetched structures in local files
        # so this is very fast
        cmd.fetch(structure[0])
        start_time = time.time()
        # actual computation
        # only take the same chains as in OpenCADD and only CA
        # altlocs are not used in computation
        res = cmd.align(
            f"{structure[0]}////ca and chain {structure[4]} and not alt A",
            f"{mobile[0]}////ca and chain {mobile[4]} and not alt A",
        )
        end_time = time.time()
        duration = round(end_time - start_time, 4)
        print(f"result: {res}")
        print(f"time: {duration}")
        cmd.reinitialize()

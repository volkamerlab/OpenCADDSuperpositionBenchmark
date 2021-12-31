"""
This script is used to parse the logfiles created by the alignment scripts for pymol.
It saves the results in a csv for further analysis like in the notebooks.
The path for the logfile aswell as the path for the resulting *.csv file need to be adjusted appropriately.
For this project the csv file is saved in the `data/PyMol_results` folder.
"""

from numpy import e
import pandas as pd
import ast

with open("<PATH_TO_LOG_FILE>") as f:
    lines = f.readlines()

ref_list = []
ref_name = []
ref_group = []
ref_species = []
ref_chain = []
ref_size_list = []
mob_list = []
mob_name = []
mob_group = []
mob_species = []
mob_chain = []
mob_size_list = []
rmsd_list = []
cov_list = []
time_list = []

w0 = 1.5  # set the normalization factor of MI to 1.5 analog to the other methods
method = "pymol"

df = pd.DataFrame(
    columns=[
        "reference_id",
        "mobile_id",
        "method",
        "rmsd",
        "coverage",
        "reference_size",
        "mobile_size",
        "time",
        "SI",
        "MI",
        "SAS",
        "ref_name",
        "ref_group",
        "ref_species",
        "ref_chain",
        "mob_name",
        "mob_group",
        "mob_species",
        "mob_chain",
    ]
)


# parsing of the file
for line in lines:
    if line.startswith("reference: "):
        ref = line.split(": ")[1]
        ref_info = ast.literal_eval(ref)
        ref_list.append(ref_info[0])
        ref_name.append(ref_info[1])
        ref_group.append(ref_info[2])
        ref_species.append(ref_info[3])
        ref_chain.append(ref_info[4])
    elif line.startswith("reference_size: "):
        ref_size_list.append(int(line.split(" ")[1]))
    elif line.startswith("mobile: "):
        mob = line.split(": ")[1]
        mob_info = ast.literal_eval(mob)
        mob_list.append(mob_info[0])
        mob_name.append(mob_info[1])
        mob_group.append(mob_info[2])
        mob_species.append(mob_info[3])
        mob_chain.append(mob_info[4])
    elif line.startswith("mobile_size: "):
        mob_size_list.append(int(line.split(" ")[1]))
    elif line.startswith("result: "):
        result = line.split(": (")
        result = ast.literal_eval(result[1][:-2])
        # use the next two lines for results with refinement
        # rmsd_list.append(round(float(result[0]), 4))
        # cov_list.append(int(result[1]))

        # use the next two lines for resutls without refinement
        rmsd_list.append(round(float(result[3]), 4))
        cov_list.append(int(result[4]))
    elif line.startswith("time: "):
        time_list.append(float(line.split(" ")[1]))

for entry in range(len(ref_list)):
    si = (rmsd_list[entry] * min(ref_size_list[entry], mob_size_list[entry])) / cov_list[entry]
    mi = 1 - (
        (1 + cov_list[entry])
        / ((1 + (rmsd_list[entry] / w0)) * (1 + min(ref_size_list[entry], mob_size_list[entry])))
    )
    sas = (rmsd_list[entry] * 100) / cov_list[entry]

    df.loc[entry] = [
        ref_list[entry],
        mob_list[entry],
        method,
        rmsd_list[entry],
        cov_list[entry],
        ref_size_list[entry],
        mob_size_list[entry],
        time_list[entry],
        si,
        mi,
        sas,
        ref_name[entry],
        ref_group[entry],
        ref_species[entry],
        ref_chain[entry],
        mob_name[entry],
        mob_group[entry],
        mob_species[entry],
        mob_chain[entry],
    ]

df.to_csv("<PATH_FOR_RESULT.csv>", mode="w", header=False, index=False)

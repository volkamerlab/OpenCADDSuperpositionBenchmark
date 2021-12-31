"""
This script is used to parse the resulting logfile of ChimeraX after performing the alignments.
It saves the results in a csv for further analysis like in the notebooks.
The path for the logfile aswell as the path for the resulting *.csv file need to be adjusted appropriately.
For this project the csv file is saved in the `data/ChimeraX_results` folder.
"""

import pandas as pd
import numpy as np


# get the logfile
with open("<PATH_TO_LOGFILE>") as f:
    lines = f.readlines()

    ref_ids = []
    ref_names = []
    ref_groups = []
    ref_species_list = []
    ref_chains = []
    mob_ids = []
    mob_names = []
    mob_groups = []
    mob_species_list = []
    mob_chains = []
    residuesize_list = []
    alignment_list = []
    cov_list = []
    rmsd_list = []
    time_list = []

    # iterate over the lines
    for line in lines:
        # get metadata for reference structure
        if "reference: " in line:
            line = line.split(";")
            ref_ids.append(line[1][:-5])
            ref_names.append(line[3][:-5])
            ref_groups.append(line[5][:-5])
            ref_species_list.append(line[7][:-5])
            ref_chains.append(line[9][:-5])
        # get metadata for mobile structure
        elif "mobile: " in line:
            line = line.split(";")
            mob_ids.append(line[1][:-5])
            mob_names.append(line[3][:-5])
            mob_groups.append(line[5][:-5])
            mob_species_list.append(line[7][:-5])
            mob_chains.append(line[9][:-5])
        # get size of structure
        elif "residues," in line:
            try:
                res = line.split(" ")
                residuesize_list.append(int(res[10]))
            except:
                print(line)
        elif line.startswith("alignment: "):
            alignment_list.append(line.split(" ")[1])
        # get RMSD and coverage of the alignment
        elif line.startswith("RMSD"):
            line = line.split(" ")
            cov_list.append(int(line[2]))
            rmsd_list.append(float(line[6]))  # without cutoff
        # when the coverage is really low, we take the values from this line. Should not occur in best case.
        elif "Fewer" in line:
            cov_list.append(0)
            rmsd_list.append(0)
        # get the time required to compute the alignment
        elif "time: " in line:
            time_list.append(float(line.split(" ")[1]))


# create emptry dataframe
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

counter_struc = 0
method = "matchmaker"
w0 = 1.5

counter = 0
# iterate through the alignments and append them to the dataframe
for al in range(len(alignment_list)):
    ref = ref_ids[al]
    ref_size = residuesize_list[al + counter_struc]
    counter_struc += 1
    mob = mob_ids[al]
    mob_size = residuesize_list[al + counter_struc]

    rmsd = round(rmsd_list[al], 4)
    cov = cov_list[al]
    time = round(time_list[al], 4)

    # when coverage and RMSD are 0, the quality measures can not be computed
    if cov == 0 and rmsd == 0:
        si = np.nan
        mi = np.nan
        sas = np.nan
    # compute quality measures
    else:
        si = round((rmsd * min(ref_size, mob_size)) / cov, 4)
        mi = round(1 - ((1 + cov) / ((1 + (rmsd / w0)) * (1 + min(ref_size, mob_size)))), 4)
        sas = round((rmsd * 100) / cov, 4)

    ref_name = ref_names[al]
    ref_group = ref_groups[al]
    ref_species = ref_species_list[al]
    ref_chain = ref_chains[al]
    mob_name = mob_names[al]
    mob_group = mob_groups[al]
    mob_species = mob_species_list[al]
    mob_chain = mob_chains[al]

    # append alignment to dataframe
    df.loc[al] = [
        ref,
        mob,
        method,
        rmsd,
        cov,
        ref_size,
        mob_size,
        time,
        si,
        mi,
        sas,
        ref_name,
        ref_group,
        ref_species,
        ref_chain,
        mob_name,
        mob_group,
        mob_species,
        mob_chain,
    ]

    counter += 1

# write dataframe to file
df.to_csv("<PATH_FOR_RESULT.csv>", mode="w", header=False, index=False)

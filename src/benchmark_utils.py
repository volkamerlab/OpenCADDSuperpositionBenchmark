"""
Provides functions used to perform the alignments by the methods in OpenCADD for the benchmark.
The functions are called in the benchmark notebooks.
"""

import pandas as pd
import numpy as np
from opencadd.structure.core import Structure
from opencadd.structure.superposition import api
import time

pd.set_option("display.max_columns", None)


def run_alignments(sample1_path=None, sample2_path=None, output_path=None, w0=1.5):
    """
    Parsing of the sample sets and iterating over the structures and the methods to perform all alignments and compute the quality measures.

    Parameters
    ----------
    sample1_path: str, Optional
        Path for the file containing the first sample set.

    sample2_path: str, Optional
        Path for the file containing the second sample set.

    output_path: str, Optional
        Path for the file containing the output of the alignments in csv format.

    w0: float, Optional
        The value for the normalization factor for MI. Default is set to 1.5.

    Returns
    -------
    None

    .. note::

        When only one sample path is provided, the alignments are performed between the strucutres of this sample set.
        When two sample paths are provided, the alignments are performed between the structures of the different sample sets.
    """

    # parsing of the sample sets
    sample_strucs1 = []
    with open(str(sample1_path)) as f:
        # split line, so no newline characters are left
        # then split lines into lists to get the same structure as in the benchmark for OpenCADD
        temp = f.read().splitlines()
        for line in temp:
            struc = line.split(",")
            sample_strucs1.append(struc)

    if sample2_path:
        sample_strucs2 = []
        with open(str(sample2_path)) as f:
            # split line, so no newline characters are left
            # then split lines into lists to get the same structure as in the benchmark for OpenCADD
            temp = f.read().splitlines()
            for line in temp:
                struc = line.split(",")
                sample_strucs2.append(struc)

    # create empty DataFrame
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
    counter = 0
    except_counter = 0

    # perfrom alignments between two sample sets
    if sample2_path:
        for method in api.METHODS:

            # structures in the sample dataset
            for structure in sample_strucs1:
                # only need to download once for every method, because the variable is put into a list.
                # the compute function operates on the entry of the list, which does not change the original strucutre here
                reference_structure = Structure.from_pdbid(structure[0])

                for mobile in sample_strucs2:
                    mobile_structure = Structure.from_pdbid(mobile[0])
                    benchmarking_structures = [reference_structure, mobile_structure]
                    df, counter, except_counter = compute_alignment(
                        method,
                        benchmarking_structures,
                        structure,
                        mobile,
                        w0,
                        counter,
                        except_counter,
                        df,
                    )
    # perform alignments between structures of one sample set
    else:
        for method in api.METHODS:

            # structures in the sample dataset
            for structure in sample_strucs1:
                # only need to download once for every method, because the variable is put into a list.
                # the compute function operates on the entry of the list, which does not change the original strucutre here
                reference_structure = Structure.from_pdbid(structure[0])

                for mobile in sample_strucs1[sample_strucs1.index(structure) + 1 :]:
                    mobile_structure = Structure.from_pdbid(mobile[0])
                    benchmarking_structures = [reference_structure, mobile_structure]
                    df, counter, except_counter = compute_alignment(
                        method,
                        benchmarking_structures,
                        structure,
                        mobile,
                        w0,
                        counter,
                        except_counter,
                        df,
                    )
    print(counter)
    print(except_counter)

    # write DataFrame
    df.to_csv(str(output_path), mode="w", header=False, index=False)


def compute_alignment(
    method, benchmarking_structures, structure, mobile, w0, counter, except_counter, df
):
    """
    Perform the alignment of the pair of structures and the method provided.
    MDA and Theseus both use Clustal Omega as the sequence alignment tool.

    Parameters
    ----------
    method: str
        Name of the method, that is used for this alignment.

    benchmarking_structures: list
        Contains the Strucutes as MDAnalysis.Universe.

    structure: list
        Contains various information of the reference structure, like the chain that will be used or the PDB-ID.

    mobile: list
        Contains various information of the mobile structure, like the chain that will be used or the PDB-ID.

    w0: float
        The value for the normalization factor for MI. Default is set to 1.5.

    counter: int
        Counts the number of alignments. This is used to see the progress.

    except_counter: int
        Counts the occurences of excepts while performing all alignments. 0 means, that there were no problems performing the alignemnts.

    df: Pandas.DataFrame
        The DataFrame where the results are stored.

    Returns
    -------
    df: Pandas.DataFrame
        The DataFrame where the results are stored.
    counter: int
        Counts the number of alignments. This is used to see the progress. 
    except_counter: int
        Counts the occurences of excepts while performing all alignments. 0 means, that there were no problems performing the alignemnts.
    """

    print(counter, method, structure, mobile)
    try:
        if method == "mda":
            start_time = time.time()
            result = api.align(
                benchmarking_structures,
                method=api.METHODS[method],
                alignment_strategy="clustalo",
                user_select=[
                    f"backbone and name CA and segid {structure[4]}",
                    f"backbone and name CA and segid {mobile[4]}",
                ],
            )
            end_time = time.time()
        elif method == "theseus":
            start_time = time.time()
            result = api.align(
                benchmarking_structures,
                method=api.METHODS[method],
                sequence_alignment="CLUSTALO",
                user_select=[
                    f"backbone and name CA and segid {structure[4]}",
                    f"backbone and name CA and segid {mobile[4]}",
                ],
            )
            end_time = time.time()
        else:
            start_time = time.time()
            result = api.align(
                benchmarking_structures,
                method=api.METHODS[method],
                user_select=[
                    f"backbone and name CA and segid {structure[4]}",
                    f"backbone and name CA and segid {mobile[4]}",
                ],
            )
            end_time = time.time()

        # if no alignment is found, set quality measures to NaN and add entry to DF
        if result[0]["scores"]["coverage"] == 0:
            df.loc[counter] = [
                structure[0],
                mobile[0],
                method,
                result[0]["scores"]["rmsd"],
                result[0]["scores"]["coverage"],
                result[0]["metadata"]["reference_size"],
                result[0]["metadata"]["mobile_size"],
                round(end_time - start_time, 4),
                np.nan,
                np.nan,
                np.nan,
            ]
        # else calculate quality measures
        else:
            si = (result[0]["scores"]["rmsd"] * min(result[0]["metadata"]["reference_size"],
                                                    result[0]["metadata"]["mobile_size"])) / result[0]["scores"]["coverage"]
            mi = 1 - ((1 + result[0]["scores"]["coverage"]) / ((1 + result[0]["scores"]["rmsd"] / w0) * (1 + min(result[0]["metadata"]["reference_size"], 
                                                                                                                 result[0]["metadata"]["mobile_size"]))))
            sas = (result[0]["scores"]["rmsd"] * 100) / result[0]["scores"]["coverage"]

            # add alignment entry to DataFrame
            df.loc[counter] = [
                structure[0],
                mobile[0],
                method,
                result[0]["scores"]["rmsd"],
                result[0]["scores"]["coverage"],
                result[0]["metadata"]["reference_size"],
                result[0]["metadata"]["mobile_size"],
                round(end_time - start_time, 4),
                si,
                mi,
                sas,
                structure[1],
                structure[2],
                structure[3],
                structure[4],
                mobile[1],
                mobile[2],
                mobile[3],
                mobile[4],
            ]
    except:
        # If there is an error, the counter is incremented and printed at the end to indicate how many
        # alignments did not work.
        df.loc[counter] = [
            structure[0],
            mobile[0],
            method,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            structure[1],
            structure[2],
            structure[3],
            structure[4],
            mobile[1],
            mobile[2],
            mobile[3],
            mobile[4],
        ]
        except_counter += 1
    counter += 1
    return df, counter, except_counter

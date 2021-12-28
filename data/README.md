# Data Folder

This folder contains all relevant data for the benchmark of the OpenCADD superposition module conducted for the bachelor thesis of Julian Pipart.

## raw:

The raw folder contains the log files of ChimeraX Matchmaker and PyMol align repectively.
The logs were created by the alignment scripts in the src folder and afterwards parsed to create the *.csv files in the ChimeraX_results and PyMol resutls folders.

The PyMol logs contain both results, before and after refinement.

## ChimeraX_results:

This folder contains the *.csv files representing the Dataframes of the results for the alignments by ChimeraX Matchmaker.
The alignments are performed without refinement.

The files were used in the Jupyter Notebooks to visualise and analyse the results.

## PyMol_results:

This folder contains the *.csv files representing the Dataframes of the results for the alignments by PyMol align.
The refinement files represent the results of the alignments after refinement. The other files represent the results before the refinement.

They were used in the Jupyter Notebooks to visualise and analyse the results.

## OpenCADD results:

The three subfolders represent the three stages of the benchmark.

1. first_results: 
   
   The first results of the methods implemented in OpenCADD.
   Theseus used MUSCLE for the sequence alignment and MDA used the global alignemnt with a gap penalty of -10 for every gap.
   The alignments were performed on all chains contained in the pdb files.

2. intermediate_results:

    The alignments were performed on one chain (chain is visible in the *.csv files).
    Theseus now used Clustal Omega for the sequence alignments and MDA used the local alignment option with a gap penalty of -10 for every gap.

    Additionally, the folder mda_parameter_tests contains the results of the alignments performed by MDA using different sequence alignment parameters. 
    
    The naming is:
    METHOD_STRATEGY_GAPOPENCOST_GAPEXTENSIONCOST

3. The *.csv files in the OpenCADD_results folder:

    These are the results of the last stage of the benchmark.
    Theseus and MDA used Clustal Omega for the sequence alignments.

## figures:

This folder contains the figures used in the bachelor thesis of Julian Pipart.
The figures were created in the according Jupyter notebooks in the notebooks folder.
The figures of the other results are also represented in the Jupyter notebooks respectively.

## Structure of the *.csv files:

Each row represents an alignment.
The columns are:

1. reference_id: PDB-ID of the reference structure
2. mobile_id: PDB-ID of the mobile structure
3. method: The method used to perform the alignment
4. rmsd: The RSMD of the alignment
5. coverage: The coverage of the alignment (how many residues were used per structure)
6. reference_size: Number of residues of the reference structure
7. mobile_size: Number of residues of the mobile structure
8. time: The time required to perform the alignment in seconds
9. SI: Similarity Index
10. MI: Match Index
11. SAS: Structural Alignment Score
12. ref_name: Name of the reference Kinase
13. ref_group: Group of the reference Kinase
14. ref_species: Species of the reference Kinase
15. ref_chain: Chain of the reference Kinase used for the calculation
16. mob_name: Name of the mobile Kinase
17. mob_group: Group of the mobile Kinase
18. mob_species: Species of the mobile Kinase
19. mob_chain: Chain of the reference Kinase used for the calculation

All csv files have the same structure except the file in the ./OpenCADD_results/first_results folder.
This file contains columns 1-11.
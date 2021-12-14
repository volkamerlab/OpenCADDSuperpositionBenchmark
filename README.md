# OpenCADDSuperpositionBenchmark
This repository icludes a benchmark of the OpenCADD superposition methods[1], PyMol align[2][3] as well as ChimeraX Matchmaker[4][5].

The methods are compared by their performance of alignment of four kinase groups.
The performance is measured by three different quality measures.

The notebooks show the results of the benchmark.
A more detailed analysis is performed for the alignments between TK structures and the alignments between TK and CAMK stuctures. 

This benchmark is the topic of the bachelor thesis of Julian Pipart. 

___
## Installation of the tools

1. Download the repository
    ```
    git clone https://github.com/volkamerlab/OpenCADDSuperpositionBenchmark.git
    ```
2. Change to the appropriate branch
    ```
    git checkout superposer_benchmark
    ```
3. Follow steps below for installation of the methods.
### OpenCADD
Please follow the installation guide of [OpenCADD](https://opencadd.readthedocs.io/en/latest/installing.html). If the changes ([Pull request #117](https://github.com/volkamerlab/opencadd/pull/117)), which are made as part of the project, are not in the master branch yet, please use the [jp-superposer-extension branch](https://github.com/volkamerlab/opencadd/tree/jp-superposer-extension).

Therefore the download of the git repository is required.
```
git clone https://github.com/volkamerlab/opencadd.git
```
MMLigner requires a rebuild, please follow steps shown below while in the "jp-superposer-extension" branch:
```
conda config --add channels conda-forge 
conda activate base
conda install conda-build
conda build devtools/conda-recipes/mmligner/
conda activate OpenCADDBenchmark
conda install -c local mmligner pip
```


### PyMol
For the installation of the Open-Source PyMol, please follow the guide of the PyMolWiki:
[Linux Install](https://pymolwiki.org/index.php/Linux_Install)
[MAC Install](https://pymolwiki.org/index.php/MAC_Install)

### ChimeraX
For the installation of ChimeraX, please use their download website and follow their installation guide. (See [here](https://www.cgl.ucsf.edu/chimerax/))

___
For ChimeraX Matchmaker and PyMol align separate scripts were developed to perform the alignments and parse the output, to bring it into a readable dataframe for the analysis.
The alignments of the OpenCADD methods are performed in the notebooks.
The paths in the scripts need to be changed appropriately for your system.
___
## References
[1] Available at: https://github.com/volkamerlab/opencadd
[2] S. G. Yuan, H. C. S. Chan, and Z. Q. Hu, “Using pymol as a platform for computational drug design,”Wiley Interdisciplinary Reviews-Computational Molecular Science, vol. 7, no. 2, 2017. [Online]. Available:$<$Go to ISI$>$$:$//WOS:000399013100006
[3] Schrödinger, LLC, “The PyMOL molecular graphics system, version 1.8,” November 2015.
[4] E. C. Meng, E. F. Pettersen, G. S. Couch, C. C. Huang, and T. E. Ferrin, “Tools for integratedsequence-structure analysis with ucsf chimera,”BMC Bioinformatics, vol. 7, p. 339, 2006. [Online].Available:  https://www.ncbi.nlm.nih.gov/pubmed/16836757
[5]  E. F. Pettersen, T. D. Goddard, C. C. Huang, E. C. Meng, G. S. Couch, T. I. Croll, J. H. Morris, andT. E. Ferrin, “Ucsf chimerax:  Structure visualization for researchers, educators, and developers,”ProteinSci, vol. 30, no. 1, pp. 70–82, 2021. [Online]. Available:  https://www.ncbi.nlm.nih.gov/pubmed/32881101

___
## Acknowledgements
Thank you to all the members of the Volkamer Lab for the great opportunity of conduction my bachelor thesis here.

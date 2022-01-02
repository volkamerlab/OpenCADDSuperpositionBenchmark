# OpenCADDSuperpositionBenchmark
This repository icludes a benchmark of the OpenCADD superposition methods[1], PyMol align[2][3] as well as ChimeraX Matchmaker[4, 5].

The methods are compared by their performance of alignment of four kinase groups.
The structures are queried from the Kinase-Ligand Interactions Fingerprints and Structures database (KLIFS). [6, 7, 8]
The performance is measured and compared by the three quality measures SI [9, 10], MI [9, 10] and SAS [10, 11].


The jupyter notebooks [12] show the results of the benchmark.
For analysing the results, the following Python libraries were mainly used:

- Pandas (V 1.3.5) [13, 14]
- Matplotlib (V 3.5.1) [15]
- Seaborn (V 0.11.2) [16]
- SciPy (V 1.7.3) [17]
- NumPy (V 1.21.5) [18]
- statsmodels (V 0.13.1) [19]
  
The Python version 3.8.12 was used for this project.

A more detailed analysis is performed for the alignments between TK structures and the alignments between TK and CAMK stuctures. 

This benchmark is the topic of the bachelor thesis of Julian Pipart. 

___
## Installation of the tools
For the installation, Conda [20] and PyPI pip [21] are required.

1. Download the repository:
    ```
    git clone https://github.com/volkamerlab/OpenCADDSuperpositionBenchmark.git
    ```

2. Change the directory the OpenCADDSuperpositionBenchmark folder.
    ```
    cd OpenCADDSuperpositionBenchmark
    ```

3. Create the conda environment:
This environment.yml is based on the environment.yml of OpenCADD and includes additions for this benchmark.
It extends the OpenCADD environment file. So no additional environment for this benchmark should be required.
    ```
    conda env create -f OpenCADDSuperpositionBenchmark.yml
    ```

4. Follow steps below for installation of the methods.

### OpenCADD
IMPORTANT: The benchmark was performed with changes made in OpenCADD, which are in the [jp-superposer-extension branch](https://github.com/volkamerlab/opencadd/tree/jp-superposer-extension). So the guide will explain how to use this branch for recreation.

Make sure to change the directory, so you are not in the local OpenCADDSuperpositionBenchmark repository.

Therefore, the download of the git repository is required:
```
git clone https://github.com/volkamerlab/opencadd.git
```
Change the directory the OpenCADDSuperpositionBenchmark folder.
```
cd opencadd
```
Next, the branch is changed to "jp-superposer-extension":
```
git checkout jp-superposer-extension
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
Afterwards the superposer module can be installed locally:
```
pip install . 
```
To see if it was successful, one can check with the following command:
```
superposer -h
```


### PyMol
For the installation of the Open-Source PyMol, please follow the guide of the PyMolWiki:
- [Linux Install](https://pymolwiki.org/index.php/Linux_Install)
- [MAC Install](https://pymolwiki.org/index.php/MAC_Install)

### ChimeraX
For the installation of ChimeraX, please use their download website and follow their installation guide. (See [here](https://www.cgl.ucsf.edu/chimerax/download.html))

___
For ChimeraX Matchmaker and PyMol align separate scripts were developed to perform the alignments and parse the output, to bring it into a readable dataframe for the analysis.
The alignments of the OpenCADD methods are performed in the jupyter notebooks.
The paths in the scripts need to be changed appropriately for your system.
Subfolders contain additional README files to explain, what data they contain. 
___
## References
[1] Available at: https://github.com/volkamerlab/opencadd \
[2] S. G. Yuan, H. C. S. Chan, and Z. Q. Hu, “Using pymol as a platform for computational drug design,” Wiley Interdisciplinary Reviews-Computational Molecular Science, vol. 7, no. 2, 2017. [Online]. Available:<Go to ISI>://WOS:000399013100006 \
[3] Schrödinger, LLC, “The PyMOL molecular graphics system, version 1.8,” November 2015. \
[4] E. C. Meng, E. F. Pettersen, G. S. Couch, C. C. Huang, and T. E. Ferrin, “Tools for integrated sequence-structure analysis with ucsf chimera,” BMC Bioinformatics, vol. 7, p. 339, 2006. [Online]. Available:  https://www.ncbi.nlm.nih.gov/pubmed/16836757 \
[5] E. F. Pettersen, T. D. Goddard, C. C. Huang, E. C. Meng, G. S. Couch, T. I. Croll, J. H. Morris, and T. E. Ferrin, “Ucsf chimerax: Structure visualization for researchers, educators, and developers,” ProteinSci, vol. 30, no. 1, pp. 70–82, 2021. [Online]. Available:  https://www.ncbi.nlm.nih.gov/pubmed/32881101
[6] O. P. van Linden, A. J. Kooistra, R. Leurs, I. J. de Esch, and C. de Graaf, “Klifs:  a knowledge-based structural database to navigate kinase-ligand interaction space,”J Med Chem, vol. 57, no. 2, pp. 249–77,2014. [Online]. Available:  https://www.ncbi.nlm.nih.gov/pubmed/23941661
[7] A. J. Kooistra, G. K. Kanev, O. P. van Linden, R. Leurs, I. J. de Esch, and C. de Graaf, “Klifs:  a structural kinase-ligand interaction database,” Nucleic Acids Res, vol. 44, no. D1, pp. D365–71, 2016.[Online]. Available:  https://www.ncbi.nlm.nih.gov/pubmed/26496949
[8] G. K. Kanev, C. de Graaf, B. A. Westerman, I. J. P. de Esch, and A. J. Kooistra, “Klifs:  an overhaul after the first 5 years of supporting kinase research,” Nucleic Acids Res, vol. 49, no. D1, pp. D562–D569,2021. [Online]. Available: https://pubmed.ncbi.nlm.nih.gov/33084889/
[9] G. J. Kleywegt and T. A. Jones, “A super position,” ESF/Ccp4 Newsletter, vol. 31, pp. 9–14, 1994.
[10] R. Kolodny, P. Koehl, and M. Levitt, “Comprehensive evaluation of protein structure alignment methods: Scoring by geometric measures,” Journal of Molecular Biology, vol. 346, no. 4, pp. 1173–1188, 2005.[Online]. Available:  https://www.sciencedirect.com/science/article/pii/S002228360401602X
[11] S. Subbiah, D. V. Laurents, and M. Levitt, “Structural similarity of dna-binding domains of bacteriophage repressors and the globin core,” Curr Biol, vol. 3, no. 3, pp. 141–8, 1993. [Online]. Available:  https://www.ncbi.nlm.nih.gov/pubmed/15335781
[12] T. Kluyver, B. Ragan-Kelley, F. Pérez, B. Granger, M. Bussonnier, J. Frederic, K. Kelley, J. Hamrick, J. Grout, S. Corlay, P. Ivanov, D. Avila, S. Abdalla, and C. Willing, “Jupyter notebooks – a publishing format for reproducible computational workflows,” in Positioning and Power in Academic Publishing: Players, Agents and Agendas, F. Loizides and B. Schmidt, Eds.    IOS Press, 2016, pp. 87 – 90.
[13] T. pandas development team, “pandas-dev/pandas: Pandas,” Feb. 2020. [Online]. Available: https://doi.org/10.5281/zenodo.5774815
[14] Wes McKinney, “Data Structures for Statistical Computing in Python,” in Proceedings of the 9th Pythonin Science Conference, Stéfan van der Walt and Jarrod Millman, Eds., 2010, pp. 56 – 61.
[15] J. D. Hunter, “Matplotlib:  A 2d graphics environment,” Computing in Science & Engineering, vol. 9,no. 3, pp. 90–95, 2007.
[16] M. L. Waskom, “seaborn:  statistical data visualization,” Journal of Open Source Software, vol. 6, no. 60,p. 3021, 2021. [Online]. Available:  https://doi.org/10.21105/joss.03021
[17] P. Virtanen, R. Gommers, T. E. Oliphant, M. Haberland, T. Reddy, D. Cournapeau, E. Burovski, P. Peterson, W. Weckesser, J. Bright, S. J. van der Walt, M. Brett, J. Wilson, K. J. Millman, N. Mayorov,A. R. J. Nelson, E. Jones, R. Kern, E. Larson, C. J. Carey, ̇I. Polat, Y. Feng, E. W. Moore, J. VanderPlas, D. Laxalde, J. Perktold, R. Cimrman, I. Henriksen, E. A. Quintero, C. R. Harris, A. M. Archibald, A. H.Ribeiro, F. Pedregosa, P. van Mulbregt, and SciPy 1.0 Contributors, “SciPy 1.0:  Fundamental Algorithms for Scientific Computing in Python,” Nature Methods, vol. 17, pp. 261–272, 2020.
[18] C. R. Harris, K. J. Millman, S. J. van der Walt, R. Gommers, P. Virtanen, D. Cournapeau, E. Wieser, J. Taylor, S. Berg, N. J. Smith, R. Kern, M. Picus, S. Hoyer, M. H. van Kerkwijk, M. Brett, A. Haldane, J. F. del Río, M. Wiebe, P. Peterson, P. Gérard-Marchant, K. Sheppard, T. Reddy, W. Weckesser, H. Abbasi, C. Gohlke, and T. E. Oliphant, “Array programming with NumPy,” Nature, vol. 585, no.7825, pp. 357–362, Sep. 2020. [Online]. Available:  https://doi.org/10.1038/s41586-020-2649-2
[19] S. Seabold and J. Perktold, “statsmodels:  Econometric and statistical modeling with python,” in 9th Python in Science Conference, 2010.
[20] “Conda documentation,”. [Online]. Available:  https://docs.conda.io/projects/conda/en/latest/index.html
[21] “pip documentation,”. [Online]. Available: [https://pip.pypa.io/en/stable/](https://pip.pypa.io/en/stable/#)


___
## Acknowledgements
Thank you to all the members of the Volkamer Lab for the great opportunity of conduction my bachelor thesis here.

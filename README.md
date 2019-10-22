# iGEMMarburg2019

This is iGEM team Marburgs 2019 GitHub Repository.<br/>
Detailed information on the project can be found on [our Wiki](https://2019.igem.org/Team:Marburg).<br/>
Our software is provided open-source under the GNU General Public License version 3 (GLPv3) and our hardware is provided open-source under the CERN Open Hardware Licence version 1.2 (CERN OHL).

## Software

### Models

#### aNSo - artificial Neutral integration Site option
This folder contains a Python script to find artificial Neutral integration Site options in a genome. Furthermore, it contains the input data used to find aNSo in the genome of *Synechococcus elongatus* UTEX 2973, such as the genome sequenced by [Yu et al., 2015](https://doi.org/10.1038/srep08132) as a FASTA file and a GenBank (gbk) file comprising all genes and TSS with their positions identified in a transcriptomics study by [Tan et al., 2018](https://doi.org/10.1186/s13068-018-1215-8), and the generated results for *S. elongatus*.

To run this script Python 3 is required, using the modules SeqIO from Bio, pandas, re and os.

#### Growth Curve Model
Model utilizes scikit learn and uses polynomial regression to predict doubling times.
The number of parameters given to the script to train is unlimited, there is no train test split or crossvalidation implemented, but it can be easily added.

#### Terminator Model

Kinetics and thermodynamic data for an already filtered list of natural intrinsic terminators of S. elongatus UTEX 2973. The data was mostly generated using MFOLD and KineFold.  
A. Xayaphoummine, T. Bucher & H. Isambert,  
Kinefold web server for RNA/DNA folding path and structure prediction including pseudoknots and knots,
Nucleic Acid Res., 33, 605-610 (2005)

M. Zuker, D. H. Mathews & D. H. Turner.  
Algorithms and Thermodynamics for RNA Secondary Structure Prediction: A Practical Guide
In RNA Biochemistry and Biotechnology, 11-43,  
J. Barciszewski and B. F. C. Clark, eds.,  
NATO ASI Series, Kluwer Academic Publishers, Dordrecht, NL, (1999)



### Colony Picking GUI and GUIDE (Graphical User Interface for Directed Engineering)

#### Colony Picking GUI

A simple graphical user interface for our implimentation of colony picking in Opentron OT-2. Its implemented in Python and uses the kivy libraries. Please keep in mind that this is a alpha version and still contains bug. We will continuously improve this over the upcoming months.

#### GUIDE (Graphical User Interface for Directed Engineering)

An easy to use graphical user interface for the overview and execution of OT-2 protocols.
It was created in C sharp for the BioHackathon2019 organised by iGEM Vilnius.
Please keep in mind that this is an alpha version and therefore might contain bugs.


### Promega Plasmid Purification Protocols
The iGEM team Marburg 2019 automated Plasmid Purification for Opentrons OT-2 using the Wizard® MagneSil® Plasmid Purification System. This folder contains one Python script and one Jupyter Notebook to run the Plasmid Purification with a p300 Single-Channel Electronic Pipette for up to six samples and another Python script and Jupyter Notebook for the use of a p300 8-Channel Electronic Pipette for up to 48 samples.

The user just has to change the variable "amount" to the number of samples for the Single Pipette or the number of used columns of a 96 Deep Well Plate for the 8-Channel Pipette.

```
amount = 6
```



### Marburg Colony Identification Neural Network (MCoINN)

In the `AI` folder you can find the AI which is used to detect colonies in images.

## Hardware
In this folder all STL files and further instructions for assembling the 3D printed hardware can be found. This includes hardware for the Colony Picking add-on, the Promega Plasmid Purification Protocols as well as additional labware.










### Authors and Copyright
iGem Marburg 2019

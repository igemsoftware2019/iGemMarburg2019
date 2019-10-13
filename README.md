# iGEMMarburg2019

This is iGEM team Marburgs 2019 GitHub Repository.<br/>
Detailed information on the project can be found on [our Wiki](https://2019.igem.org/Team:Marburg).<br/>
Our software is provided open-source under the GNU General Public License version 3 (GLPv3) and our hardware is provided open-source under the CERN Open Hardware Licence version 1.2 (CERN OHL).



## aNSo - artificial Nuclear integration Site option
This folder contains a Python script to find artificial Nuclear integration Site options in a genome. Furthermore, it contains the input data used to find aNSo in the genome of *Synechococcus elongatus* UTEX 2973, such as the genome sequenced by [Yu et al., 2015](https://doi.org/10.1038/srep08132) as a FASTA file and a GenBank (gbk) file comprising all genes and TSS with their positions identified in a transcriptomics study by [Tan et al., 2018](https://doi.org/10.1186/s13068-018-1215-8), and the generated results for *S. elongatus*.

To run this script Python 3 is required, using the modules SeqIO from Bio, pandas, re and os.


## The Trained Colony Picker AI



## GUI and Cloning Protocols



## Hardware
In this folder all STL files and further instructions for assembling the 3D printed hardware can be found. This includes hardware for the Colony Picking add-on, the Promega Plasmid Purification Protocols as well as additional labware.


## Promega Plasmid Purification Protocols
The iGEM team Marburg 2019 automated Plasmid Purification for Opentrons OT-2 using the Wizard® MagneSil® Plasmid Purification System. This folder contains one Python script to run the Plasmid Purification with a p300 Single-Channel Electronic Pipette for up to six samples and another Python script for the use of a p300 8-Channel Electronic Pipette for up to 48(?) samples.

The user just has to change the variable "amount" to the number of samples for the Single Pipette or the number of used columns of a 96 Deep Well Plate for the 8-Channel Pipette.

```
amount = 6
```










### Authors and Copyright
iGem Marburg 2019

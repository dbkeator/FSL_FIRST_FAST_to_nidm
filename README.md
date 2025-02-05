# fsl_seg_to_nidm
A tool to convert structural segmentation outputs from FSL's FIRST and FAST tool to NIDM.
It takes the output of the "simple1" container and workflow which provides the results of
FSL-based structural segmentation and provides them in a .json format. The ***fslsegstats2nidm***
program them converts these to NIDM which it can also add to the NIDM of the BIDS data structure.

# Installation
1. Create a 'clean' environment

```
$ conda create -n my_env python=3
```

2. Activate this environment

```
$ conda activate my_env
```

3. Install 'click' (since it for some reason dosent install with the main setup)

```
$ pip install click
```

4. Clone this repo
```
git clone https://github.com/ReproNim/fsl_seg_to_nidm.git
```
5. Run the setup script
```
$ cd fsl_seg_to_nidm
$ python setup.py install
```
6. Done!

# Usage
You can get information about how to run this tool by executing:
```
$ fslsegstats2nidm --help
usage: fslsegstats2nidm.py [-h] (-d DATA_FILE | -f SEGFILE) -subjid SUBJID -o
                          OUTPUT_DIR [-j] [-add_de] [-n NIDM_FILE]
                          [-forcenidm]

This program will load in JSON output from FSL's FAST/FIRST
                                        segmentation tool, augment the FSL anatomical region designations with common data element
                                        anatomical designations, and save the statistics + region designations out as
                                        NIDM serializations (i.e. TURTLE, JSON-LD RDF)

options:
  -h, --help            show this help message and exit
  -d DATA_FILE, --data_file DATA_FILE
                        Path to FSL FIRST/FAST JSON data file
  -f SEGFILE, --seg_file SEGFILE
                        Path or URL to a specific FSL JSONstats file. Note,
                        currently this is tested on ReproNim data
  -subjid SUBJID, --subjid SUBJID
                        If a path to a URL or a stats fileis supplied via the
                        -f/--seg_file parameters then -subjid parameter must
                        be set withthe subject identifier to be used in the
                        NIDM files
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        Output filename with full path
  -j, --jsonld          If flag set then NIDM file will be written as JSONLD
                        instead of TURTLE
  -add_de, --add_de     If flag set then data element data dictionary will be
                        added to nidm file else it will written to aseparate
                        file as fsl_cde.ttl in the output directory (or same
                        directory as nidm file if -n paramemteris used.
  -n NIDM_FILE, --nidm NIDM_FILE
                        Optional NIDM file to add segmentation data to.
  -forcenidm, --forcenidm
                        If adding to NIDM file this parameter forces the data
                        to be added even if the participantdoesnt currently
                        exist in the NIDM file.
```
FSL data is ready to annotate if you ran both FSL FIRST and FAST using a reproducible container (https://pubmed.ncbi.nlm.nih.gov/28781753/, https://github.com/ReproNim/simple_workflow). If FIRST and FAST were run out-of-the-box, use the fsl2jon.py script in the root of this project directory to generate the segstats.json files. For example:

```
python fsl2json.py root_of_fsl_derivatives_directroy
```
e.g.
```
python fsl2json.py ~/Desktop/proj/derivatives/fsl/  
```
Note: To run this script FSL needs to be locally installed.

Next, generate annotated FSL data with the following command:
```
fslsegstats2nidm -add_de -d segstat_file -subjid sub-01 -o output 
```
e.g.
```
fslsegstats2nidm -add_de -d ./proj/derivatives/fsl/sub-01/segstats.json -subjid sub-01 -o ./proj/derivatives/fsl/sub-01/fsl_nidm.ttl 
```

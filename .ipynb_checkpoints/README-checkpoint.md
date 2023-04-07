# Guide to running sequence-structure-function pipeline

- Collection of jupyter notebook scripts demonstrating various aspects of pipeline.
- Conda enviornments required to run pipeline and jupyter notebooks are located in conda_yml.
    - seq_struct_func.yml for steps 1,5,6
    - alphafold2.yml for step 2
    - steps 3 and 4 require an environment with pyCHARMM and MMTSB to be installed     
        - https://academiccharmm.org/documentation/latest/pycharmm
        - https://chemrxiv.org/engage/chemrxiv/article-details/63c6b40230e3e5222e937adc 
        - https://github.com/BrooksResearchGroup-UM/pyCHARMM-Workshop
        - http://feig.bch.msu.edu/mmtsb/Main_Page
- Recommended resources: 1 GPU and 1-4 CPUs
- Scripts are listed in the order they should be run.

### Data: (si_data/)     Data necessary for running examples 
- asr_seq_annotations.xlsx
    - All enzymes, sequences, and annotations from structure-function pipeline
- extant_msa.fasta
    - Multiple sequence alignment used previously to construct ancestral sequence resurrects
- fasta/
    - Sequences in asr_seq_annotations.xlsx written as fasta format
- pdb_with_fad/
    - Directory containing all AlphaFold2 models with FAD cofactor
- top_dock_pose/
    - Directory cotaining lowest energy poses from minimization in explicit protein
- log_reg_models/
    - Pretrained statsmodels logistic regression models 

### Toppar: (toppar/)   CHARMM Topology and Parameter files 

### Step 1: (consensus/) Generating consensus sequence hits library
- script/gen_consensus_db.ipynb 
    - Create database of consensus sequence hits from AlphaFold2 MSAs

### Step 2: (model/)     Generating AlphaFold2 Structures
- script/run_alphafold_consensus.ipynb 
    - Run example protein with AlphaFold2 using consensus sequence hits

### Step 3: (cofactor/)  Adding FAD Cofactor
- script/fad.ipynb
    - Add FAD cofactor into generated example protein

### Step 4: (dock/)      Docking Array of Ligands
- script/fftdock.ipynb
    - Use CHARMM Fast Fourier Transform Docking to get initial positions of ligand
- script/prot_min.ipynb
    - Refine FFT poses in explicit protein representation
- script/cluster.ipynb
    - Cluster poses to select representative poses

### Step 5: (pred/)      Prediction of Stereochemistry and Reactivity
- script/stereo.ipynb
    - Predict stereochemistry from boltzmann weighted representative poses
- script/reactivity.ipynb
    - Predict reactivity from pose features
- script/vis_pred.ipynb
    - Visuallize predicted poses 

### Step 6: (seq_func/)   Training Sequence-Function Model and SHAP Analysis
- script/run_automl.ipynb
    - Fit multiple sequence alignment to predicted stereochemistry labels with gradient boosted trees and random forest models
- script/shap_analysis.ipynb
    - Calculate SHAP values for residues and visuallize how residues affect stereochemistry 


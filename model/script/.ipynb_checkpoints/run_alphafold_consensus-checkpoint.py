"""Modified AlphaFold2 script utilizing user MSA"""
#https://github.com/deepmind/alphafold/blob/main/run_alphafold.py 

import os
os.chdir('/home/azamh/demo/seq_struct_func/model')

import json
import pathlib
import pickle
import random
import sys
import time
import shutil
from typing import Dict

from absl import app
from absl import flags
from absl import logging
import numpy as np

from alphafold.common import protein
from alphafold.data import pipeline
from alphafold.data import parsers
from alphafold.data import templates
from alphafold.data import tools
from alphafold.model import data
from alphafold.model import config
from alphafold.model import model
from alphafold.relax import relax
from alphafold.data.tools import jackhmmer

logging.set_verbosity(logging.INFO)

#AlphaFold params:
num_ensemble = 1
RELAX_MAX_ITERATIONS = 0
RELAX_ENERGY_TOLERANCE = 2.39
RELAX_STIFFNESS = 10.0
RELAX_EXCLUDE_RESIDUES = []
RELAX_MAX_OUTER_ITERATIONS = 20

#Paths to FASTA files, each containing one sequence. Paths should be separated by commas. 
#All FASTA paths must have a unique basename as the  basename is used to name the output directories for each prediction.
fasta_paths = ['../si_data/fasta/tropb.fasta']
#Path to a directory that will store the results.
output_dir = './models'
#Path to custom sequence database
custom_db_path = '../consensus/consensus_db.fasta'
#Names of models to use.
model_names = ['model_1']
#Path to directory of supporting data.
data_dir = '/export/apps/CentOS7/alphafold/data'
#Path to the JackHMMER executable.
jackhmmer_binary_path = shutil.which('jackhmmer')
#Path to the HHsearch executable.
hhsearch_binary_path = shutil.which('hhsearch')
#Path to the Kalign executable.
kalign_binary_path = shutil.which('kalign')
#database for use by HHsearch.
pdb70_database_path = os.path.join(data_dir, "pdb70/pdb70")
#template mmCIF structures, each named <pdb_id>.cif
template_mmcif_dir = os.path.join(data_dir, "pdb_mmcif/mmcif_files")
#Maximum template release date to consider. Important if folding historical test sets.
max_template_date = '2022-01-01'
#Path to file containing a mapping from obsolete PDB IDs to the PDB IDs of their replacements.
obsolete_pdbs_path = os.path.join(data_dir, "pdb_mmcif/obsolete.dat")
#The random seed for the data 
#pipeline. By default, this is randomly generated. Note 
#that even if this is set, Alphafold may still not be 
#deterministic, because processes like GPU inference are 
#nondeterministic.
random_seed = None
#Save MSA generated from JackHMMER
save_msa = True

#Generate model and msa directories:
fasta_names = [pathlib.Path(p).stem for p in fasta_paths]
if len(fasta_names) != len(set(fasta_names)):
    raise ValueError('All FASTA paths must have a unique basename.')
model_dirs = []
msa_dirs = []
for fasta_path, fasta_name in zip(fasta_paths, fasta_names):
    model_dir = os.path.join(output_dir, fasta_name)
    msa_dir = os.path.join(model_dir, 'msa')
    os.makedirs(msa_dir, exist_ok = True)
    model_dirs.append(model_dir)
    msa_dirs.append(msa_dir)

### Generate MSA and Templates ###
def gen_feature_dict_database(fasta_path, msa_output_dir):

    #parse input sequence
    logging.info(f'Constructing feature dictionary')
    with open(fasta_path) as f:
        input_fasta_str = f.read()
    input_seqs, input_descs = parsers.parse_fasta(input_fasta_str)
    if len(input_seqs) != 1:
        raise ValueError(
            f'More than one input sequence found in {input_fasta_str}.')
    input_sequence = input_seqs[0]
    input_description = input_descs[0]
    num_res = len(input_sequence)
    
    #generate and parse msa
    logging.info('Generating MSA')
    max_hits = 10000
    jackhmmer_runner = jackhmmer.Jackhmmer(
        binary_path=jackhmmer_binary_path,
        database_path=custom_db_path)
    jackhmmer_result = jackhmmer_runner.query(
        fasta_path)[0]
    msa_as_a3m = parsers.convert_stockholm_to_a3m(
        jackhmmer_result['sto'], max_sequences=max_hits)
    msa, deletion_matrix, _ = parsers.parse_stockholm(
            jackhmmer_result['sto'])
    msa = msa[:max_hits]
    deletion_matrix = deletion_matrix[:max_hits]
    
    if save_msa:
        with open(os.path.join(msa_output_dir, 'msa_jackhmmer.sto'), 'w') as f:
            f.write(jackhmmer_result['sto'])
        
    #parse templates: use jackhmmer msa to find templates with hhsearch
    logging.info('Searching for templates)')
    hhsearch_pdb70_runner = tools.hhsearch.HHSearch(binary_path=hhsearch_binary_path, databases=[pdb70_database_path])
    hhsearch_result = hhsearch_pdb70_runner.query(msa_as_a3m)
    hhsearch_hits = parsers.parse_hhr(hhsearch_result)
    
    if save_msa:
        with open(os.path.join(msa_output_dir, 'hhsearch_hits'), 'w') as f:
            for hit in hhsearch_hits:
                #each hit is an instance of class TemplateHit in data.parsers
                f.write('>' + hit.name + '\n')
                f.write(hit.hit_sequence + '\n')
    
    template_featurizer = templates.TemplateHitFeaturizer(
        mmcif_dir=template_mmcif_dir,
        max_template_date=max_template_date,
        max_hits=MAX_TEMPLATE_HITS,
        kalign_binary_path=kalign_binary_path,
        release_dates_path=None,
        obsolete_pdbs_path=obsolete_pdbs_path)
        
    templates_result = template_featurizer.get_templates(
            query_sequence=input_sequence,
            query_pdb_code=None,
            query_release_date=None,
            hits=hhsearch_hits)
    
    #generate feature_dict for model
    feature_dict = {**pipeline.make_sequence_features(sequence=input_sequence, description=input_description, num_res=num_res),
                **pipeline.make_msa_features(msas=[msa], deletion_matrices=[deletion_matrix]),
                **templates_result.features}
    
    return feature_dict

#Run AlphaFold pipeline
def model_inference(model_runners, 
                    feature_dict,
                    model_dir):
    
    #Score models by plddts
    plddts = {}
    unrelaxed_proteins = {}

    # Run the models.
    for model_name, model_runner in model_runners.items():
        logging.info('Running model %s', model_name)
        t_0 = time.time()
        processed_feature_dict = model_runner.process_features(
            feature_dict, random_seed=random_seed)

        t_0 = time.time()
        prediction_result = model_runner.predict(processed_feature_dict)
        t_diff = time.time() - t_0
        logging.info(
            'Total JAX model %s predict time (includes compilation time, see --benchmark): %.0fs',
            model_name, t_diff)
        
        # Get mean pLDDT confidence metric.
        plddts[model_name] = np.mean(prediction_result['plddt'])

        # Save the model outputs.
        result_output_path = os.path.join(model_dir, f'result_{model_name}.pkl')
        with open(result_output_path, 'wb') as f:
            pickle.dump(prediction_result, f, protocol=4)

        unrelaxed_protein = protein.from_prediction(processed_feature_dict,
                                                    prediction_result)
        unrelaxed_proteins[model_name] = unrelaxed_protein

        unrelaxed_pdb_path = os.path.join(model_dir, f'unrelaxed_{model_name}.pdb')
        with open(unrelaxed_pdb_path, 'w') as f:
            f.write(protein.to_pdb(unrelaxed_protein))

    return plddts, unrelaxed_proteins

#Relax model with amber
def amber_relaxation(unrelaxed_proteins, amber_relaxer, model_dir):
    # Relax the predictions.
    relaxed_pdbs = {}
    for model_name, unrelaxed_protein in unrelaxed_proteins.items():
        t_0 = time.time()
        relaxed_pdb_str, _, _ = amber_relaxer.process(prot=unrelaxed_protein)
        relaxed_pdbs[model_name] = relaxed_pdb_str

        # Save the relaxed PDB.
        relaxed_output_path = os.path.join(model_dir, f'relaxed_{model_name}.pdb')
        with open(relaxed_output_path, 'w') as f:
            f.write(relaxed_pdb_str)
    return relaxed_pdbs

#Rank models by plddt values
def rank_models(plddts, relaxed_pdbs, model_dir):
    # Rank by pLDDT and write out relaxed PDBs in rank order.
    ranked_order = []
    for idx, (model_name, _) in enumerate(
        sorted(plddts.items(), key=lambda x: x[1], reverse=True)):
        ranked_order.append(model_name)
        ranked_output_path = os.path.join(model_dir, f'ranked_{idx}.pdb')
        with open(ranked_output_path, 'w') as f:
            f.write(relaxed_pdbs[model_name])

    ranking_output_path = os.path.join(model_dir, 'ranking_debug.json')
    with open(ranking_output_path, 'w') as f:
        f.write(json.dumps({'plddts': plddts, 'order': ranked_order}, indent=4))
    return ranked_order

#Run AlphaFold for all fasta files
if random_seed is None:
    random_seed = random.randrange(sys.maxsize)
    
for fasta_path, model_dir, msa_dir in zip(fasta_paths, model_dirs, msa_dirs):
    #Path to feature dict saved as pickle file
    features_output_path = os.path.join(model_dir, 'features.pkl')

    #Run AlphaFold
    logging.info(f'Running AlphaFold for {fasta_path}')

    #Construct feature dictionary that contains MSA and template information
    if not os.path.isfile(features_output_path):
        feature_dict = gen_feature_dict_database(fasta_path, msa_dir)
        with open(features_output_path, 'wb') as f:
            pickle.dump(feature_dict, f, protocol=4)
    else:
        feature_dict = pickle.load(open(features_output_path, 'rb'))
        logging.info('Feature dictionary already generated')

    #Run AlphaFold model inference
    model_runners = {}
    for model_name in model_names:
        model_config = config.model_config(model_name)
        model_config.data.eval.num_ensemble = num_ensemble
        model_params = data.get_model_haiku_params(
            model_name=model_name, data_dir=data_dir)
        model_runner = model.RunModel(model_config, model_params)
        model_runners[model_name] = model_runner

    logging.info('Have %d models: %s', len(model_runners),
                list(model_runners.keys()))
    plddts, unrelaxed_proteins = model_inference(model_runners, feature_dict, model_dir)

    #Perform amber relaxation
    amber_relaxer = relax.AmberRelaxation(
        max_iterations=RELAX_MAX_ITERATIONS,
        tolerance=RELAX_ENERGY_TOLERANCE,
        stiffness=RELAX_STIFFNESS,
        exclude_residues=RELAX_EXCLUDE_RESIDUES,
        max_outer_iterations=RELAX_MAX_OUTER_ITERATIONS)
    relaxed_pdbs = amber_relaxation(unrelaxed_proteins, amber_relaxer, model_dir)

    #Rank models
    ranked_order = rank_models(plddts, relaxed_pdbs, model_dir)

        


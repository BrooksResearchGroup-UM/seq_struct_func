#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Refine FFTDock poses via minimization in explicit protein
import os 
import re
import pandas as pd
import numpy as np
os.environ['CHARMM_LIB_DIR'] = "/home/azamh/charmm-dev/lib"

# These are a subset of the pycharmm modules that were installed when
# pycharmm was installed in your python environment
import pycharmm
import pycharmm.generate as gen
import pycharmm.ic as ic
import pycharmm.coor as coor
import pycharmm.energy as energy
import pycharmm.dynamics as dyn
import pycharmm.nbonds as nbonds
import pycharmm.minimize as minimize
import pycharmm.crystal as crystal
import pycharmm.image as image
import pycharmm.psf as psf
import pycharmm.read as read
import pycharmm.write as write
import pycharmm.settings as settings
import pycharmm.cons_harm as cons_harm
import pycharmm.cons_fix as cons_fix
import pycharmm.select as select
import pycharmm.shake as shake
import pycharmm.settings as settings
import pycharmm.grid as grid
import pycharmm.charmm_file as charmm_file
from pycharmm.select_atoms import SelectAtoms
from pycharmm.lingo import charmm_script

from pycharmm.lib import charmm as libcharmm

os.chdir('/home/azamh/demo/seq_struct_func/dock')


#Arguments
protein = 'tropb'
ligand = '2'
toppardir = '../toppar'
liganddir = './ligands'
proteindir = '../cofactor/pdb_with_fad'
fftdockdir = f'poses/{protein}_{ligand}_fftdock'
dockdir = f'poses/{protein}_{ligand}_prot'
os.makedirs(dockdir, exist_ok=True)

## Read in the topology and parameter file 
settings.set_bomb_level(-1)
read.rtf(os.path.join(toppardir, 'top_all36_prot.rtf'))
read.rtf(os.path.join(toppardir,'top_all36_cgenff.rtf'), append = True)
read.rtf(os.path.join(toppardir,'probes.rtf'), append = True)
read.prm(os.path.join(toppardir, 'par_all36m_prot.prm'), flex = True)
read.prm(os.path.join(toppardir, 'par_all36_cgenff.prm'), append = True, flex = True)
read.prm(os.path.join(toppardir, 'probes.prm'), append = True, flex = True)
settings.set_bomb_level(0)
charmm_script(f'stream {os.path.join(liganddir, ligand)}.str')
charmm_script(f'stream {os.path.join(toppardir, "st2_fadh.str")}')


#Build ligand
ligand_pdb = os.path.join(liganddir, f'{ligand}.pdb')
read.sequence_pdb(ligand_pdb)
gen.new_segment(seg_name = "LIGA")
read.pdb(ligand_pdb, resid = True)

#Setup nonbonds
my_nbonds = pycharmm.NonBondedScript(
    cutnb=12.0, ctonnb=10.0, ctofnb=10.0,
    eps=0.75,
    cdie=False,
    rdie=True,
    switch=True, vswitch=True)
# Implement these non-bonded parameters by "running" them.
my_nbonds.run()

#Minimize ligand in vacuum
minimize.run_sd(nstep=1000, tolenr=1e-3, tolgrd=1e-4)


## Build protein
protein_psf = os.path.join(proteindir, f'{protein}_fad.psf')
protein_pdb = os.path.join(proteindir, f'{protein}_fad.pdb')
read.psf_card(protein_psf, append = True)
read.pdb(protein_pdb, resid = True)

#Fix protein and cofactor atoms
cons_fix.setup(selection = ~SelectAtoms(seg_id='LIGA'))


#Get initial energy of system by translating ligand away from protein
charmm_script('coor tranlate xdir 400 ydir 400 zdir 400 select segid LIGA end')

#Get initial energy
def get_energy_df(pose_name):
    df = energy.get_energy().set_index('name').drop(columns = 'feature').transpose()
    df.index = [pose_name]
    df.index.name = 'pose'
    df.columns.name = 'term'
    return df
initial_energy_df = get_energy_df('initial')
print(initial_energy_df)

#Minimize all fftdock poses
nsave = 2
pose_energy_dfs = [initial_energy_df]
for i in range(1, nsave + 1):
    print(i)
    
    #Read FFTDock pose
    fftdock_pose = os.path.join(fftdockdir, f'{protein}_{ligand}_{i}.crd')
    read.pdb(fftdock_pose, resid=True)
    energy.show()
    
    #Perform minimization in explicit protein
    minimize.run_sd(nstep=50)
    minimize.run_abnr(nstep=1000, tolenr = 1e-3)

    #Get refined energy
    pose_energy_df = get_energy_df(i)
    pose_energy_dfs.append(pose_energy_df)

    #write pdb
    pose_pdb = os.path.join(dockdir, f'{protein}_{ligand}_{i}.pdb')
    write.coor_pdb(pose_pdb, sele = 'segid LIGA end')
    
#Concat energy dataframes
energy_df = pd.concat(pose_energy_dfs).fillna(0)
energy_df

#Get final-initial energy
delta_energy_df = energy_df.subtract(energy_df.loc['initial'].values, axis = 1)
delta_energy_df

#Save energies
scorefile = f'scores/{protein}_{ligand}_prot.csv'
delta_energy_df.to_csv(scorefile)




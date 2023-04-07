#Use FFTDock to dock ligands into AlphaFold models with FAD cofactor
#Inputs:
    #cofactor/pdb_with_fad/tropb.pdb
    #dock/ligands/2.pdb
    #dock/ligands/2.str #CGenFF stream file
    #toppar
    #dock/inp
#Outputs:
    #dock/grid/tropb_fftdock_3.bin
    #dock/poses/tropb_2_fftdock_3
    #dock/poses/tropb_2_prot_0.75
    #dock/scores/
    
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

## Read in grid box information
xcen = 57.135381
ycen = 45.1752381
zcen = 46.0617619
maxlen = 12

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


## Build protein
protein_psf = os.path.join(proteindir, f'{protein}_fad.psf')
protein_pdb = os.path.join(proteindir, f'{protein}_fad.pdb')
read.psf_card(protein_psf, append = True)
read.pdb(protein_pdb, resid = True)

## Generate grids
gridfile = f'grid/{protein}_fftdock.bin'
probefile = os.path.join(toppardir, 'fftdock_c36prot_cgenff_probes.txt')
cdocker = grid.CDOCKER()
settings = {'xCen' : xcen, 'yCen' : ycen, 'zCen' : zcen, 
            'xMax' : maxlen, 'yMax' : maxlen, 'zMax' : maxlen,
            'emax' : 2, 'maxe' : 40, 'mine' : -20, 'flag_gpu' : True, 
            'gridFile' : gridfile, 'dielec' : 3, 'flag_rdie' : True,
            'probeFile' : probefile} 
cdocker.setVar(settings)
cdocker.generate()

## Prepare system
ligand_pdb = os.path.join(liganddir, f'{ligand}.pdb')
psf.delete_atoms(pycharmm.SelectAtoms().all_atoms())
read.sequence_pdb(ligand_pdb)
gen.new_segment(seg_name = "LIGA")
read.pdb(ligand_pdb, resid = True)

#Get initial energy
initial_energy_df = energy.get_energy().set_index('name')
print(initial_energy_df)

#Read grid 
charmm_script(f"open unit 30 read unform name {gridfile}")
charmm_script("fftg read unit 30")

#Read list of rotations
quaternion_set = os.path.join(toppardir, 'fftdock_rotation_1.qua')
charmm_script(f"open unit 31 read form name {quaternion_set}")

#Perform FFTDock
nsave = 500
charmm_script(f"fftg lcon ncon 1 icon 1  nrok {nsave} quau 31 sizb 100 select segid LIGA end")
charmm_script("close unit 31")

#Load grid for pose score
charmm_script(f'''
open unit 1 read unform name {gridfile}
grid read unit 1 select all end
close unit 1
''')

#Go through each rotation
for i in range(1, 2):
    print(i)
    
    #Set rotation
    charmm_script(f'fftg coor icon 1 irot {i}')
    
    #Calculate energy
    print(energy.get_energy())

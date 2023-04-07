#Use FFTDock and refinment to dock ligands into AlphaFold models with FAD cofactor
import os 

#Define protein and ligand to dock
charmm_exec = '/home/wyujin/CHARMM7/stable-release/install/test/bin/charmm'
protein = 'tropb'
ligand = '2'
liganddir = './ligands'
faddir = '../cofactor/pdb_with_fad'
fftdock_dockdir = os.path.join('poses', f'{protein}_{ligand}_fftdock_3')
fftdock_eps = 3
griddir = './grid'
scriptdir = './inp'
fftdock_poses = 500
fftdock_scorefile = f'scores/{protein}_{ligand}_fftdock_3.dat'

#Create directory for fftdock poses
os.makedirs(fftdock_dockdir, exist_ok = True)

#Run FFTDock
#Generate FFTDOCK conformers
def fftdock(protein: str,
            ligand: str,
            dockdir: str,
            scorefile: str,
            epsilon: int,
            griddir:str,
            scriptdir:str,
            faddir:str,
            liganddir:str,
            num_poses:int):
    
    #generate fftdock grid with fftdock.inp
    gridfile = f'{griddir}/{protein}_fftdock_{epsilon}.bin'
    if not os.path.isfile(gridfile):
        grid_gen_out = os.popen(f'{charmm_exec} -i {scriptdir}/fftdock.inp makegrid=1 protein={protein} epsilon={epsilon} scriptdir={scriptdir} faddir={faddir} gridfile={gridfile}').read()
        print(grid_gen_out)
        
        if not os.path.isfile(gridfile):
            raise ValueError('Grid Generation Failed! See CHARMM Out')
    
    #generate fftdock conformations
    fftdock_out = os.popen(f'{charmm_exec} -i {scriptdir}/fftdock.inp griddock=1 protein={protein} faddir={faddir} liganddir={liganddir} ' + 
                           f'ligand={ligand} poses={num_poses}  dockdir={dockdir} scorefile={scorefile} epsilon={epsilon} gridfile={gridfile} scriptdir={scriptdir}').read()
    print(fftdock_out)
    
    return
fftdock(protein, ligand, fftdock_dockdir, fftdock_scorefile, fftdock_eps, griddir, scriptdir, faddir, liganddir, fftdock_poses)


#Minimize fftdock poses in explicit protein
prot_dockdir = os.path.join('poses', f'{protein}_{ligand}_prot_0.75')
prot_eps = 0.75
prot_scorefile = f'scores/{protein}_{ligand}_prot_0.75.dat'

#Minimize fftdock poses in explicit protein
def prot(protein: str,
         ligand: str,
         dockdir: str,
         scorefile: str,
         eps_study: int,
         fftdockdir: str,
         scriptdir:str,
         faddir:str,):
    
    #Minimize on explicit protein 
    prot_min_out = os.popen(f'{charmm_exec} -i {scriptdir}/protmin.inp protein={protein} ligand={ligand} poses={fftdock_poses} ' + 
        f'dockdir={dockdir} scorefile={scorefile} faddir={faddir} ' + 
        f'fftdockdir={fftdockdir} epsilon={eps_study} scriptdir={scriptdir}').read()
    print(prot_min_out)
    
    return
prot(protein, ligand, prot_dockdir, prot_scorefile, prot_eps, fftdock_dockdir, scriptdir, faddir)
